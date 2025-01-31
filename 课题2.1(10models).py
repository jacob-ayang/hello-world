import pandas as pd

# 读取数据
df = pd.read_excel('某市二手房交易数据集.xlsx')
df_ref = pd.read_excel('对照表.xlsx')

# 查看数据集的列名
print(df.columns)
print(df_ref.columns)