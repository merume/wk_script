# 国土数値情報、文部科学省の学校データから小学校、中学区のデータを抽出する
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

shp_school = gpd.read_file('./data/P29-21.shp')
csv1_school = pd.read_csv('./data/220124-mxt-mxt_chousa01-1000011635_3.csv')
csv2_school = pd.read_csv('./data/220124-mxt-mxt_chousa01-1000011635_6.csv')

# データフレームを結合
combined_school = pd.concat([csv1_school, csv2_school])

school = pd.merge(shp_school, combined_school, left_on='P29_002', right_on='学校コード', how='inner')

# P29_003 = 16001, 16002  小学校：16001 中学校：1602
# P29_007 = 1 開校中
sh = school[(school['P29_003'].isin([16001, 16002])) & (school['P29_007']==1)]

for index, school_infro in sh.head(5).iterrows():
    print('------------')
    print('学校コード： %s' % (school_infro['P29_002']))
    print('学校名：%s' % (school_infro['学校名']))
    print('学校所在地：%s' % (school_infro['学校所在地']))
    print('郵便番号：%s' % (school_infro['郵便番号']))
    print('緯度：%s' % (school_infro['geometry'].x))
    print('経度：%s' % (school_infro['geometry'].y))
    #print('------')
    #print(school_infro)

print('------------')
print('データ件数：%s' % (sh.shape[0]))
print('ダウンロードデータ')
print('国土数値情報：%s' % (shp_school[shp_school['P29_003'].isin([16001, 16002])].shape[0]))
print('文部科学省 東日本：%s' % (csv1_school[csv1_school['学校種'].isin(['B1', 'C1'])].shape[0]))
print('文部科学省 西日本：%s' % (csv2_school[csv2_school['学校種'].isin(['B1', 'C1'])].shape[0]))
print('文部科学省 計：%s' % (combined_school[combined_school['学校種'].isin(['B1', 'C1'])].shape[0]))
