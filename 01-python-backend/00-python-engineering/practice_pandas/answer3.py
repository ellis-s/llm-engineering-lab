"""
考查： 去重判断、用户粒度与记录粒度、groupby、merge、排序。
"""

from pathlib import Path

import pandas as pd

file_path = Path(__file__).parent / "用户下单数据.csv"

data = pd.read_csv(file_path, encoding="gbk")
print(data.head(), data.dtypes)

data["用户出生日期"] = pd.to_datetime(data["用户出生日期"])

"""
检查 订单ID 的重复情况，列出所有重复 ID 的记录，比较整行重复与仅 ID 重复。假定目前无法判定这些不同记录是否应合并，后续一律保留。
"""
print("=" * 20)
print("整行重复: ", data.duplicated().sum())

print("仅ID重复：", data.duplicated(subset=["订单ID"]).sum())
print(data[data.duplicated(subset=["订单ID"])])


"""
按 用户ID 统计下单记录数、总交易金额、平均单笔金额、首次和最近下单时间，并计算至少有 2 条记录的用户数及其占全部用户数的比例。
"""
print("=" * 20)

user_group = data.groupby(by=["用户ID"]).agg(
    下单记录数=("订单ID", "size"),
    总交易金额=("交易金额", "sum"),
    平均单笔金额=("交易金额", "mean"),
    首次下单时间=("下单时间", "min"),
    最近下单时间=("下单时间", "max"),
)

print(user_group)
two_more_count = len(user_group[user_group["下单记录数"] >= 2])
print(
    "至少有 2 条记录的用户数 = ",
    two_more_count,
    "\n",
    f"占比 = {two_more_count / len(user_group) * 100:.2f}%",
)


"""
先检查每个用户的 性别、婚姻状况、文化程度 是否分别一致；若不一致则提示并停止，不要任意挑选资料。用用户画像表和用户汇总表进行一对一合并。
"""

print("=" * 20)

fields = ["性别", "婚姻状况", "文化程度"]
data_1 = data.groupby(by=["用户ID"])[fields].nunique(dropna=False)
print(data_1)
confilict = data_1.gt(1).any(axis=1)

print(confilict)
