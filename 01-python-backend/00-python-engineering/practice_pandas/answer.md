# Pandas 综合实战题参考答案

题目见 [question.md](question.md)。以下是一种解法；在本文件所在目录运行。先运行一次“公共准备”，再运行任意一道题的代码块。每题重新读取数据，不依赖其他题的结果。需要 `pandas`、`openpyxl` 和 `matplotlib`。

## 公共准备

```python
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path('files')
CSV = DATA / '用户下单数据.csv'
XLSX = DATA / '电商销售数据.xlsx'


def read_orders():
    return pd.read_csv(
        CSV, encoding='gbk',
        dtype={'用户ID': 'string', '订单ID': 'string'}
    )


def read_sales(sheet='销售数据'):
    return pd.read_excel(XLSX, sheet_name=sheet, dtype={'订单号': 'string'})


def split_region(df):
    # 返回副本，原始“区域”列保留，拆分后清除首尾空格。
    df = df.copy()
    parts = df['区域'].str.split('-', n=2, expand=True)
    parts = parts.apply(lambda col: col.str.strip())
    df[['大区', '省份', '城市']] = parts
    return df


def price_number(col):
    return pd.to_numeric(
        col.astype('string').str.replace('¥', '', regex=False).str.strip(),
        errors='coerce'
    )
```

## 题 1：销售数据质量检查与清洗

```python
raw = read_sales('销售数据_清洗')
print('形状：', raw.shape)
print('数据类型：\n', raw.dtypes)
print('各列缺失：\n', raw.isna().sum())
print('整行重复数：', raw.duplicated().sum())
print('订单号重复数：', raw.duplicated(subset=['订单号']).sum())

clean = raw.drop_duplicates().copy()
comparison = pd.DataFrame({
    '清洗前': [len(raw), raw['销售额'].sum(), raw['利润'].sum()],
    '清洗后': [len(clean), clean['销售额'].sum(), clean['利润'].sum()],
}, index=['记录数', '销售额', '利润'])
comparison['减少'] = comparison['清洗前'] - comparison['清洗后']
print(comparison)

clean['日期'] = pd.to_datetime(clean['日期'], errors='raise')
clean = split_region(clean)
clean['进货价格_数值'] = price_number(clean['进货价格'])
clean = clean.fillna({'客户性别': '未知', '商品品类': '未知品类'})

by_gender = clean.groupby('客户性别', as_index=False).agg(
    记录数=('订单号', 'size'), 销售额=('销售额', 'sum')
)
print(by_gender)
print('未填写的数值字段：\n', clean[['客户年龄', '销售数']].isna().sum())
print('分组与全表销售额相等：',
      np.isclose(by_gender['销售额'].sum(), clean['销售额'].sum(), rtol=0, atol=1e-6))
print(clean[['区域', '大区', '省份', '城市', '进货价格', '进货价格_数值']].head())
```

**核对：** 原表 7,290 行、完全重复 6 行；去重后 7,284 行。销售额从 590,239,210 减至 589,973,980，利润从 122,957,160 减至 122,906,330。原表缺失包括客户性别 9、客户年龄 5、商品品类 4、销售数 5。缺失销售数并不等于销量为 0；分类缺失填充只是为了保留汇总口径。

## 题 2：订单消费画像与分箱

```python
orders = read_orders()
orders['用户出生日期'] = pd.to_datetime(
    orders['用户出生日期'], format='%Y/%m/%d', errors='raise'
)
orders['下单时间'] = pd.to_datetime(
    orders['下单时间'], format='%Y/%m/%d %H:%M', errors='raise'
)
orders['近似年龄'] = 2024 - orders['用户出生日期'].dt.year
orders['年龄段'] = pd.cut(
    orders['近似年龄'], bins=[0, 30, 40, 50, 100],
    labels=['(0,30]', '(30,40]', '(40,50]', '(50,100]'], right=True
)
print('未分箱记录数：', orders['年龄段'].isna().sum())
profile = orders.groupby(['年龄段', '性别'], observed=True, as_index=False).agg(
    记录数=('用户ID', 'size'), 用户数=('用户ID', 'nunique'),
    交易额=('交易金额', 'sum'), 平均金额=('交易金额', 'mean')
)
print(profile.round({'交易额': 2, '平均金额': 2}))

# 不指定固定标签：分位点重复被删除时，标签数量仍然匹配。
orders['金额四分组'], edges = pd.qcut(
    orders['交易金额'], q=4, duplicates='drop', retbins=True
)
quartiles = orders.groupby('金额四分组', observed=True).agg(
    记录数=('交易金额', 'size'), 最小金额=('交易金额', 'min'),
    最大金额=('交易金额', 'max'), 平均金额=('交易金额', 'mean')
)
print('分箱边界：', edges)
print(quartiles.round(2))

threshold = orders['交易金额'].quantile(0.9)
high = orders.loc[orders['交易金额'] > threshold]
print(f'90%分位数：{threshold:.6f}')
print(f'严格高于阈值：{len(high)} 条，占比 {len(high) / len(orders):.2%}')
print(f'高价值记录平均金额：{high["交易金额"].mean():.2f}')
```

**核对：** 未分箱 0 条；各年龄段记录数依次为 891、1,633、1,628、848。90% 分位数约 955.141327，严格大于该值的记录有 500 条，平均金额约 1,054.50。用户可能有多条订单，不能把这 500 条称为 500 位高价值用户。`qcut` 的分位点相同时，`duplicates='drop'` 可能使实际分组数少于 4。

## 题 3：复购用户与用户级消费榜

```python
orders = read_orders()
orders['下单时间'] = pd.to_datetime(
    orders['下单时间'], format='%Y/%m/%d %H:%M', errors='raise'
)
print('整行重复数：', orders.duplicated().sum())
print('订单ID重复数（除第一次之外）：', orders.duplicated('订单ID').sum())
print('所有重复ID对应记录：\n',
      orders.loc[orders.duplicated('订单ID', keep=False)]
            .sort_values(['订单ID', '下单时间']).to_string(index=False))

users = orders.groupby('用户ID', as_index=False).agg(
    记录数=('订单ID', 'size'), 总交易额=('交易金额', 'sum'),
    平均单笔=('交易金额', 'mean'), 首次下单=('下单时间', 'min'),
    最近下单=('下单时间', 'max')
)
users['复购用户'] = users['记录数'] >= 2
print('用户总数：', len(users))
print('至少两条记录的用户数：', users['复购用户'].sum())
print(f'占比：{users["复购用户"].mean():.2%}')

fields = ['性别', '婚姻状况', '文化程度']
consistency = orders.groupby('用户ID')[fields].nunique(dropna=False)
conflicts = consistency.gt(1).any(axis=1)
if conflicts.any():
    raise ValueError(f'用户画像存在冲突：{consistency.loc[conflicts]}')
profiles = orders[['用户ID'] + fields].drop_duplicates()
result = users.merge(profiles, on='用户ID', how='left', validate='one_to_one')
print('消费榜前10：\n',
      result.sort_values(['总交易额', '用户ID'], ascending=[False, True])
            .head(10).round({'总交易额': 2, '平均单笔': 2}).to_string(index=False))
by_gender = result.groupby('性别', dropna=False, as_index=False).agg(
    用户数=('用户ID', 'size'), 复购用户数=('复购用户', 'sum'),
    人均累计消费=('总交易额', 'mean')
)
print(by_gender.round({'人均累计消费': 2}))
```

**核对：** 原始记录 5,000 条、整行重复 0 条、重复订单 ID 的额外记录 2 条，涉及 2 个 ID；用户 2,462 人，其中 1,532 人有至少两条记录。ID 重复而其他字段不同，不能未经确认就按 ID 去重；本题的复购是记录层面的近似定义。

## 题 4：大区与品类经营分析及表格重塑

```python
sales = split_region(read_sales('销售数据'))
sales['日期'] = pd.to_datetime(sales['日期'], errors='raise')
summary = sales.groupby(['大区', '商品品类'], as_index=False).agg(
    记录数=('订单号', 'size'), 销售数=('销售数', 'sum'),
    销售额=('销售额', 'sum'), 利润=('利润', 'sum')
)
summary['利润率%'] = summary['利润'].div(summary['销售额'].replace(0, np.nan)) * 100
print('大区品类汇总：\n', summary.round({'利润率%': 2}))

top3 = (summary.sort_values(['大区', '销售额', '商品品类'],
                            ascending=[True, False, True])
               .groupby('大区', sort=False).head(3))
print('各大区前3品类：\n', top3.round({'利润率%': 2}))

wide = pd.pivot_table(sales, index='大区', columns='商品品类',
                      values='销售额', aggfunc='sum', fill_value=0)
long = wide.reset_index().melt(id_vars='大区', var_name='商品品类',
                               value_name='销售额')
print('销售额透视表：\n', wide.to_string())
print('还原的长表：\n', long)
print('销售额合计一致：', np.isclose(long['销售额'].sum(), sales['销售额'].sum(),
                                    rtol=0, atol=1e-6))

categories = sales.groupby('商品品类', as_index=False).agg(
    销售额=('销售额', 'sum'), 利润=('利润', 'sum')
)
categories['销售额占比%'] = categories['销售额'] / sales['销售额'].sum() * 100
print(categories.sort_values('销售额', ascending=False).round({'销售额占比%': 2}))
```

**核对：** 原表销售额 589,973,980、利润 122,906,330；销售额最高的品类为床品件套，销售额 109,509,440。总利润 ÷ 总销售额是以销售额为权重的整体利润率；直接平均逐条利润率会给不同金额的记录相同权重，通常不等价。透视后补 0 可能额外产生不存在的“大区-品类”组合，不会改变总额。

## 题 5：每日销售趋势与可视化

```python
import matplotlib.pyplot as plt

sales = read_sales('销售数据')
sales['日期'] = pd.to_datetime(sales['日期'], errors='raise').dt.normalize()
daily = sales.groupby('日期').agg(
    记录数=('订单号', 'size'), 销售额=('销售额', 'sum'), 利润=('利润', 'sum')
).sort_index()
calendar = pd.date_range(daily.index.min(), daily.index.max(), freq='D', name='日期')
daily = daily.reindex(calendar, fill_value=0)
daily['销售额_7日均值'] = daily['销售额'].rolling(7, min_periods=7).mean()

# 日期已升序，idxmax 对并列最大值选择最早日期。
peak = daily['销售额'].idxmax()
first_avg = daily['销售额_7日均值'].first_valid_index()
print('销售额最高日期：', peak.date(), '销售额：', daily.loc[peak, '销售额'])
print('首个7日均值：', first_avg.date(), round(daily.loc[first_avg, '销售额_7日均值'], 2))
print(daily.round(2).to_string())

weekday = (daily.assign(星期=daily.index.dayofweek)
                .groupby('星期').agg(
                    记录数=('记录数', 'sum'), 销售额=('销售额', 'sum'),
                    自然日数=('销售额', 'size'))
                .reindex(range(7), fill_value=0))
weekday['日均销售额'] = weekday['销售额'].div(weekday['自然日数'].replace(0, np.nan))
weekday.index = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
print(weekday.round({'日均销售额': 2}))

# 如系统没有这些字体，可替换为本机已安装的中文字体。
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
ax = daily[['销售额', '销售额_7日均值']].plot(figsize=(11, 5))
ax.set(title='每日销售额与7日均值', xlabel='日期', ylabel='金额（元）')
ax.legend(['每日销售额', '7日均值'])
plt.tight_layout()
plt.savefig('每日销售趋势.png', dpi=150)
plt.close()
```

**核对：** 数据涵盖 2023-11-01 至 2023-11-30 的 30 个自然日；11 月 1 日有 224 条记录、销售额 18,462,790。销售额最高的是 11 月 11 日，为 27,643,430。首个 7 日均值出现在 11 月 7 日，约 19,907,585.71。先补齐日期再滚动，才是自然日窗口；缺少中文字体不影响统计，但可能影响图上文字显示。

## 题 6：两个工作表的订单对账

```python
sales = read_sales('销售数据')
clean_raw = read_sales('销售数据_清洗')
for name, frame in [('销售数据', sales), ('销售数据_清洗', clean_raw)]:
    print(name, '整行重复：', frame.duplicated().sum(),
          '订单号重复：', frame.duplicated('订单号').sum())

clean = clean_raw.drop_duplicates().copy()
for name, frame in [('销售数据', sales), ('销售数据_清洗去重后', clean)]:
    if frame['订单号'].isna().any() or frame['订单号'].duplicated().any():
        raise ValueError(f'{name} 的订单号为空或不唯一，请先调查')

joined = sales.merge(clean, on='订单号', how='outer', suffixes=('_销售', '_清洗'),
                     indicator=True, validate='one_to_one')
print('键匹配情况：\n', joined['_merge'].value_counts())
matched = joined.loc[joined['_merge'] == 'both'].copy()
for suffix in ['销售', '清洗']:
    matched[f'价格数值_{suffix}'] = price_number(matched[f'进货价格_{suffix}'])

both_prices = matched['价格数值_销售'].notna() & matched['价格数值_清洗'].notna()
different = both_prices & matched['价格数值_销售'].ne(matched['价格数值_清洗'])
print('价格可比较记录数：', both_prices.sum())
print('两表价格不同记录数：', different.sum())
for suffix in ['销售', '清洗']:
    cols = [f'实际售价_{suffix}', f'价格数值_{suffix}',
            f'销售数_{suffix}', f'利润_{suffix}']
    valid = matched[cols].notna().all(axis=1)
    expected = (matched.loc[valid, cols[0]] - matched.loc[valid, cols[1]]) * matched.loc[valid, cols[2]]
    mismatch = ~np.isclose(expected, matched.loc[valid, cols[3]], rtol=0, atol=1e-6)
    print(f'{suffix}：可校验 {valid.sum()}，不可校验 {(~valid).sum()}，不相等 {mismatch.sum()}')

example_cols = ['订单号'] + [
    f'{col}_{suffix}'
    for suffix in ['销售', '清洗']
    for col in ['价格数值', '实际售价', '销售数', '利润']
]
print('价格不同的示例：\n', matched.loc[different, example_cols].head(1).to_string(index=False))
```

**核对：** 两表去除完全重复后均为 7,284 个唯一订单号，全部匹配；两表进货价格不同的记录为 7,104 条。`销售数据` 的 7,284 条均可用公式校验，其中 7,104 条不相等；去重后的 `销售数据_清洗` 有 7,279 条可校验且均相等，5 条销量缺失而不可校验。公式一致只能说明数据内部一致，不能代替业务核实，也不能按物理行号关联。

## 题 7：跨数据集的关联可行性与报表

```python
orders = read_orders()
sales = read_sales('销售数据')

# 去重得到唯一键后再验证一对一；不改动用于汇总的原始记录。
left_keys = orders[['订单ID']].dropna().drop_duplicates().rename(columns={'订单ID': '键'})
right_keys = sales[['订单号']].dropna().drop_duplicates().rename(columns={'订单号': '键'})
keys = left_keys.merge(right_keys, on='键', how='outer', indicator=True,
                       validate='one_to_one')
key_counts = (keys['_merge'].value_counts()
              .reindex(['left_only', 'right_only', 'both'], fill_value=0)
              .rename_axis('匹配状态').reset_index(name='唯一键数'))
print('唯一键匹配统计：\n', key_counts)

order_gender = orders.groupby('性别', dropna=False, as_index=False).agg(
    记录数=('交易金额', 'size'), 金额合计=('交易金额', 'sum'),
    记录平均金额=('交易金额', 'mean')
)
order_gender.insert(0, '数据源', '用户下单数据')
sales_gender = sales.groupby('客户性别', dropna=False, as_index=False).agg(
    记录数=('销售额', 'size'), 金额合计=('销售额', 'sum'),
    记录平均金额=('销售额', 'mean')
).rename(columns={'客户性别': '性别'})
sales_gender.insert(0, '数据源', '电商销售数据')
gender_report = pd.concat([order_gender, sales_gender], ignore_index=True)
print('各数据集分别汇总：\n', gender_report.round({'金额合计': 2, '记录平均金额': 2}))

order_dates = pd.to_datetime(orders['下单时间'], format='%Y/%m/%d %H:%M')
sales_dates = pd.to_datetime(sales['日期'])
print('CSV下单时间范围：', order_dates.min(), '至', order_dates.max())
print('Excel销售日期范围：', sales_dates.min(), '至', sales_dates.max())

# 会覆盖当前目录下同名输出文件，不会覆盖原始附件。
with pd.ExcelWriter('综合分析报表.xlsx', engine='openpyxl') as writer:
    key_counts.to_excel(writer, sheet_name='键匹配', index=False)
    gender_report.round({'金额合计': 2, '记录平均金额': 2}).to_excel(
        writer, sheet_name='性别汇总', index=False
    )
```

**核对：** CSV 唯一订单 ID 4,998 个，Excel 唯一订单号 7,284 个，交集 0 个；但 CSV 仍按原始 5,000 条记录汇总。CSV 的下单时间最晚为 2023-06-04，Excel 是 2023 年 11 月，且 Excel 没有用户 ID。现有数据不支持把用户与商品品类关联，也无法确认两个文件构成同一业务范围；因此不能简单将金额相加作为业务总额。即使两个字段出现相同数值，也需要先核实其业务含义及关联基数。
