import pandas as pd
import numpy as np

# 读取数据
df = pd.read_excel('某市二手房交易数据集.xlsx')
df_ref = pd.read_excel('对照表.xlsx')

# 查看数据集的列名
print(df.columns)
print(df_ref.columns)

# 标准化价格和面积
min_price = df['单价（元/平方米）'].min()
max_price = df['单价（元/平方米）'].max()
min_area = df['建筑面积（平方米）'].min()
max_area = df['建筑面积（平方米）'].max()

df['Price_Score'] = 1 - (df['单价（元/平方米）'] - min_price) / (max_price - min_price)
df['Area_Score'] = (df['建筑面积（平方米）'] - min_area) / (max_area - min_area)

# 楼层评分
floor_mapping = {
    '低楼层': 0.3,
    '中楼层': 0.5,
    '高楼层': 0.7
}
df['Floor_Score'] = df['所在楼层'].str.split().str[0].map(floor_mapping)

# 装修情况评分
decoration_mapping = {
    '精装': 1,
    '简装': 0.7,
    '毛坯': 0.5,
    '其他': 0.3
}
df['Decoration_Score'] = df['装修情况'].map(decoration_mapping)

# 建筑结构评分
structure_mapping = {
    '钢混结构': 1,
    '框架结构': 0.9,
    '砖混结构': 0.7,
    '其他': 0.5
}
df['Structure_Score'] = df['建筑结构'].map(structure_mapping)

# 房型评分
room_mapping = {
    '1室1厅1厨1卫': 0.5,
    '2室2厅1厨1卫': 0.8,
    '3室2厅1厨2卫': 1,
    # 其他房型可以继续添加
}
df['Room_Score'] = df['房屋户型'].map(room_mapping)

# 物业类型评分
property_mapping = {
    '商品房': 1,
    '已购公房': 0.8,
    '拆迁安置房': 0.7,
    '其他': 0.5
}
df['Property_Score'] = df['交易权属'].map(property_mapping)

# 处理缺失值
df['Floor_Score'].fillna(0, inplace=True)
df['Decoration_Score'].fillna(0, inplace=True)
df['Structure_Score'].fillna(0, inplace=True)
df['Room_Score'].fillna(0, inplace=True)
df['Property_Score'].fillna(0, inplace=True)

# 计算总评分，每个评分项乘以1000
df['Total_Score'] = 0.4 * df['Price_Score'] * 1000 + 0.3 * df['Area_Score'] * 1000 + 0.15 * df['Floor_Score'] * 1000 + 0.1 * df['Decoration_Score'] * 1000 + 0.05 * df['Structure_Score'] * 1000 + 0.05 * df['Room_Score'] * 1000 + 0.05 * df['Property_Score'] * 1000

# 按总评分降序排序
df_sorted = df.sort_values(by='Total_Score', ascending=False)

# 输出结果
output_columns = ['序号', '单价（元/平方米）', '建筑面积（平方米）', '所在楼层', '装修情况', '建筑结构', '房屋户型', '交易权属', 'Total_Score']
df_sorted[output_columns].to_excel('性价比评分表.xlsx', index=False)

# 生成HTML文件
html_content = df_sorted[output_columns].to_html(index=False, classes='table table-striped table-bordered')

# 添加HTML头部和尾部
html_full = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>二手房性价比评分表</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        .table {{
            width: 100%;
            max-width: 100%;
            margin-bottom: 1rem;
            background-color: transparent;
        }}
        th, td {{
            padding: 0.75rem;
            vertical-align: top;
            border-top: 1px solid #dee2e6;
        }}
        th {{
            vertical-align: bottom;
            border-bottom: 2px solid #dee2e6;
        }}
        thead {{
            color: #fff;
            background-color: #007bff;
        }}
        tbody tr:nth-of-type(odd) {{
            background-color: rgba(0, 0, 0, 0.05);
        }}
    </style>
</head>
<body>
    <h1>二手房性价比评分表</h1>
    {html_content}
</body>
</html>
"""

# 保存HTML文件
with open('性价比评分表.html', 'w', encoding='utf-8') as f:
    f.write(html_full)

print("性价比评分表已生成并保存为性价比评分表.html")