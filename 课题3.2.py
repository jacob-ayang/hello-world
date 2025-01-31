import pandas as pd
import numpy as np

# 读取数据
transaction_data = pd.read_excel('C:\\Users\\jacob\\OneDrive\\文档\\课题\\某市二手房交易数据集.xlsx')
lookup_table = pd.read_excel('C:\\Users\\jacob\\OneDrive\\文档\\课题\\对照表.xlsx', sheet_name='Sheet1')

# 合并数据集
transaction_data = pd.merge(transaction_data, lookup_table, left_on='房屋地址（街道）', right_on='代号', how='left')

# 去除重复值
transaction_data.drop_duplicates(inplace=True)

# 处理缺失值
transaction_data.dropna(subset=['房屋所属市辖区', '房屋地址（街道）', '建筑面积（平方米）', '单价（元/平方米）'], inplace=True)

# 数据类型转换
transaction_data['挂牌时间'] = pd.to_datetime(transaction_data['挂牌时间'])
transaction_data['单价（元/平方米）'] = pd.to_numeric(transaction_data['单价（元/平方米）'])

# 特征工程
transaction_data['挂牌月份'] = transaction_data['挂牌时间'].dt.month
transaction_data['挂牌年份'] = transaction_data['挂牌时间'].dt.year

# 编码装修情况和房屋用途
transaction_data['装修情况'] = transaction_data['装修情况'].map({'精装修': 1, '普通装修': 0})
transaction_data['房屋用途'] = transaction_data['房屋用途'].map({'普通住宅': 1, '商业用途': 0})

# 检查装修情况和房屋用途是否成功转换
print("装修情况和房屋用途转换后的前几行:")
print(transaction_data[['装修情况', '房屋用途']].head())

# 如果装修情况和房屋用途有空值，用默认值填充
transaction_data['装修情况'] = transaction_data['装修情况'].fillna(0)
transaction_data['房屋用途'] = transaction_data['房屋用途'].fillna(0)

# 再次检查装修情况和房屋用途
print("填充空值后的装修情况和房屋用途前几行:")
print(transaction_data[['装修情况', '房屋用途']].head())

# 假设引入楼层和朝向作为新的特征
# 假设楼层和朝向的数据已经存在
# 编码楼层和朝向
transaction_data['楼层'] = transaction_data['所在楼层'].map({'低层': 1, '中层': 2, '高层': 3})
transaction_data['朝向'] = transaction_data['朝向'].map({'南': 1, '北': 0})

# 如果楼层和朝向有空值，用默认值填充
transaction_data['楼层'] = transaction_data['楼层'].fillna(0)
transaction_data['朝向'] = transaction_data['朝向'].fillna(0)

# 计算性价比评分
def calculate_score(row):
    return (
        0.3 * row['建筑面积（平方米）'] +
        0.2 * row['装修情况'] +
        0.1 * row['房屋用途'] +
        0.1 * row['楼层'] +
        0.1 * row['朝向'] +
        0.2 * (1 / (row['市中心距离'] + 1)) -
        0.1 * row['单价（元/平方米）']
    )

# 计算初始评分
transaction_data['初始评分'] = transaction_data.apply(calculate_score, axis=1)

# 计算评分的最大值和最小值
max_score = transaction_data['初始评分'].max()
min_score = transaction_data['初始评分'].min()

# 归一化评分到 [0, 100] 范围
if max_score != min_score:
    transaction_data['评分'] = ((transaction_data['初始评分'] - min_score) / (max_score - min_score)) * 100
else:
    transaction_data['评分'] = 50  # 如果所有评分相同，设置为50

# 排序和筛选
top_properties = transaction_data.sort_values(by='评分', ascending=False).head(10)

# 打印评分最高的10个房产
print("评分最高的10个房产:")
print(top_properties[['房屋地址（街道）', '建筑面积（平方米）', '装修情况', '房屋用途', '市中心距离', '单价（元/平方米）', '评分']])