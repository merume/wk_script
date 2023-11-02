# 任意の緯度経度（ポイント）の学校（学区内）の取得
# python point_to_school.py --lat 35.7764351  --long 139.6431903

import argparse
import geopandas as gpd
from shapely.geometry import Point

parser = argparse.ArgumentParser()
parser.add_argument('--long')
parser.add_argument("--lat")

args = parser.parse_args()
# 緯度経度を定義
latitude = args.lat
longitude = args.long
# 緯度経度をPointオブジェクトに変換
point = Point(longitude, latitude)

# 小学校 学区データの読み込み
elementary_school_districts = gpd.read_file('./data/A27-21_13.shp')
# 学区を特定（小学校）
district = None
for index, school_district in elementary_school_districts.iterrows():
    if school_district['geometry'].contains(point):
        district = school_district
        break

# 学区内の学校を表示
if district is not None:
    school_names = district['A27_004']
    print('通学する小学校:', school_names)
else:
    print('緯度経度が学区内にありません。')

# 中学校 学区データの読み込み
middle_school_districts = gpd.read_file('./data/A32-21_13.shp')
# 学区を特定（中学校）
district = None
for index, school_district in middle_school_districts.iterrows():
    if school_district['geometry'].contains(point):
        district = school_district
        break

# 学区内の学校を表示
if district is not None:
    school_names = district['A32_004']
    print('通学する中学校:', school_names)
else:
    print('緯度経度が学区内にありません。')
