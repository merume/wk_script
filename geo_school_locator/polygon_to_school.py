# 任意の住所（丁目まで）の学校（学区）の取得
# python polygon_to_school.py --addr '東京都目黒区目黒一丁目'
import argparse
import re
import geopandas as gpd
from shapely.geometry import Point

def divide_addess(address):
  matches = re.match(r'(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)' , address)
  return matches

parser = argparse.ArgumentParser()
parser.add_argument('--addr')

args = parser.parse_args()
# 住所の分解
matches = divide_addess(args.addr)
pref_name = matches[1]
city_name = matches[2]
s_name = matches[3]

# 丁目ポリゴンデータの読み込み
town_areas = gpd.read_file('./data/r2ka13.shp')
# エリア情報の取得
area_gdf = town_areas[(town_areas['PREF_NAME'] == pref_name) & (town_areas['CITY_NAME'] == city_name) & (town_areas['S_NAME'] == s_name)]

# 小学校 学区データの読み込み
elementary_school_districts = gpd.read_file('./data/A27-21_13.shp')

intersecting_districts = []
for index, school_district in elementary_school_districts.iterrows():
    if school_district['geometry'].intersects(area_gdf['geometry']).any():
        intersecting_districts.append(school_district)

for district in intersecting_districts:
    school_names = district['A27_004']
    print('学区内の小学校:', school_names)

# 中学校 学区データの読み込み
middle_school_districts = gpd.read_file('./data/A32-21_13.shp')

intersecting_districts = []
for index, school_district in middle_school_districts.iterrows():
    if school_district['geometry'].intersects(area_gdf['geometry']).any():
        intersecting_districts.append(school_district)

for district in intersecting_districts:
    school_names = district['A32_004']
    print('学区内の中学校:', school_names)
