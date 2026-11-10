"""
**考查：** 日期、`cut`、`qcut`、分组聚合、分位数。
"""

from pathlib import Path

import pandas as pd

file_path = Path(__file__).parent / "用户下单数据.csv"

data = pd.read_csv(file_path, encoding="gbk")
print(data.head())

"""
1. 将出生日期、下单时间转为日期时间。参照课程使用 `2024 - 出生年份` 计算近似年龄，明确这不是截至某天的精确周岁。


"""
data["用户出生日期"] = pd.to_datetime(data["用户出生日期"])
data["下单时间"] = pd.to_datetime(data["下单时间"])
print(data.dtypes)

print("=" * 20)
data["年龄"] = 2026 - data["用户出生日期"].dt.year
print(data.head())


"""
2. 将年龄分为 `(0,30]`、`(30,40]`、`(40,50]`、`(50,100]`，检查是否有未分箱记录。按年龄段、性别统计记录数、去重用户数、交易金额合计和平均值。

"""
print("=" * 20)
age_cut = pd.cut(data["年龄"], bins=[0, 30, 40, 50, 100], right=True)
print(age_cut)
print(len(age_cut), len(data))
data["年龄段"] = age_cut
print(data)
print("未分箱记录", data["年龄段"].isna().sum())

print(
    data.groupby(by=["年龄段", "性别"], as_index=False).agg(
        记录数=("用户ID", "size"),
        用户数=("用户ID", "nunique"),
        交易金额合计=("交易金额", "sum"),
        交易平均值=("交易金额", "mean"),
    )
)

"""
3. 按单笔交易金额的四分位数做四组等频分箱，展示各组记录数、金额范围及平均金额；若分位点重复，允许减少分箱数并说明原因。

"""
print("=" * 20)
data["交易金额_4等分段"], edge = pd.qcut(
    data["交易金额"], q=4, duplicates="drop", retbins=True
)
quartiles = data.groupby(by=["交易金额_4等分段"], observed=True).agg(
    记录数=("交易金额", "size"),
    最小金额=("交易金额", "min"),
    最大金额=("交易金额", "max"),
    平均金额=("交易金额", "mean"),
)

print(edge)
print(quartiles.round(2))

"""
4. 计算单笔金额的 90% 分位数，筛选严格大于阈值的记录，输出记录数、占全部记录的比例和平均金额。说明高价值**订单记录**不等同于高价值用户。
"""
print("=" * 20)

at90 = data["交易金额"].quantile(0.9)
print(at90)
vip_users = data[data["交易金额"] > at90]
print(len(vip_users), f"{len(vip_users) / len(data) * 100:.2f}%")
print(vip_users["交易金额"].mean())
