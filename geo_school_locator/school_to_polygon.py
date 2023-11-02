# 学校（学区）内の丁目の取得
# python school_to_polygon.py --school '文京区立大塚小学校'
import argparse
import re
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--school')

args = parser.parse_args()

shp_school = gpd.read_file('./data/P29-21.shp')
csv1_school = pd.read_csv('./data/220124-mxt-mxt_chousa01-1000011635_3.csv')
csv2_school = pd.read_csv('./data/220124-mxt-mxt_chousa01-1000011635_6.csv')

# データフレームを結合
combined_school = pd.concat([csv1_school, csv2_school])

school_list = pd.merge(shp_school, combined_school, left_on='P29_002', right_on='学校コード', how='inner')
school = school_list[(school_list['学校名'] == args.school)]
school_code = school['P29_002'].iloc[0] 

# 小学校 学区データの読み込み
elementary_school_districts = gpd.read_file('./data/A27-21_13.shp')
school_district = elementary_school_districts[(elementary_school_districts['A27_003'] == school_code)]

# 丁目ポリゴンデータの読み込み
town_areas = gpd.read_file('./data/r2ka13.shp')
areas = []
for index, town_area in town_areas.iterrows():
    if school_district['geometry'].intersects(town_area['geometry']).any():
        areas.append(town_area)

for area in areas:
    area_name = area['PREF_NAME']+area['CITY_NAME']+area['S_NAME']
    print('地域名:', area_name)
