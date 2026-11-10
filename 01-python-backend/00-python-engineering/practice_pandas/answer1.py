from pathlib import Path

import pandas as pd

file_path = Path(__file__).parent / "电商销售数据.xlsx"

data = pd.read_excel(file_path, sheet_name="销售数据_清洗")

print(data.head())
"""
1.读取数据，显示行列数、各列类型、各列缺失数，统计整行重复数及按 订单号 判断的重复数。
"""
print("=" * 10, "行列数", "=" * 10)
print(data.shape)

print("=" * 10, "各列类型", "=" * 10)
print(data.dtypes)

print("=" * 10, "各列缺失数", "=" * 10)
print(data.isna().sum())  # 好像默认对列进行处理？

print("=" * 10, "统计整行重复数", "=" * 10)
print(data.duplicated().sum())


print("=" * 10, "按 订单号 判断的重复", "=" * 10)
print(data.duplicated(subset=["订单号"]).sum())


"""
2. 去除完全重复行，保留第一次出现的记录；报告清洗前后记录数、销售额和利润的合计及差额。不要因订单号相同而直接删除内容不同的行。
"""
print("=" * 10, "去除完全重复行，保留第一次出现的记录", "=" * 10)
data_1 = data.drop_duplicates(keep="first")
print(data_1)

print(
    "=" * 10,
    "报告清洗前后记录数、销售额和利润的合计及差额。不要因订单号相同而直接删除内容不同的行",
    "=" * 10,
)
comparison = pd.DataFrame(
    {
        "清洗前": [len(data), data["销售额"].sum(), data["利润"].sum()],
        "清洗后": [len(data_1), data_1["销售额"].sum(), data_1["利润"].sum()],
    },
    index=["记录数", "销售额总数", "利润总数"],
)
comparison["差额(前-后)"] = comparison["清洗前"] - comparison["清洗后"]
print(comparison)


"""
3.将日期转为日期类型；把 区域 按 - 分为 大区、省份、城市，清除各部分首尾空格；把带 ¥ 的进货价格转为数值列 进货价格_数值。
"""
print("=" * 10, "将日期转为日期类型", "=" * 10)
data["日期"] = pd.to_datetime(data["日期"])
print(data["日期"].dtype)


print("=" * 10, "把 区域 按 - 分为 大区、省份、城市，清除各部分首尾空格", "=" * 10)
data[["大区", "省份", "城市"]] = data["区域"].str.split("-", expand=True)
print(data)

print("=" * 10, "把带 ¥ 的进货价格转为数值列 进货价格_数值。", "=" * 10)
data["进货价格_数值"] = data["进货价格"].str.replace("¥", "").astype(int)
print(data.head())


"""
4. 将缺失的客户性别填为 未知、商品品类填为 未知品类；保留数值字段的缺失，不编造销量或年龄。按清洗后的客户性别统计记录数和销售额，并验证分组销售额合计与清洗后全表一致。
"""
print("=" * 10, "将缺失的客户性别填为 未知、商品品类填为 未知品类", "=" * 10)
data_2 = data.fillna({"客户性别": "未知", "商品品类": "未知品类"})
print(data_2[data_2["客户性别"] == "未知"])


print("=" * 10, "按清洗后的客户性别统计记录数和销售额", "=" * 10)
data_3 = data_2.groupby(by=["客户性别"], as_index=False).agg(
    记录数=("订单号", "count"), 销售额合计=("销售额", "sum")
)
print(data_3)

print(data_3["销售额合计"].sum() == data_2["销售额"].sum())
