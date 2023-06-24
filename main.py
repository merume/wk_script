import geopandas as gpd
from shapely.geometry import Point

# 学区データの読み込み
school_districts = gpd.read_file('./data/A27-10_01-g_SchoolDistrict.shp')

# 小学校データの読み込み
schools = gpd.read_file('./data/A27-10_01-g_PublicElementarySchool.shp')
# 緯度経度を定義
latitude = 43.1789565
longitude = 141.7593046

# 緯度経度をPointオブジェクトに変換
point = Point(longitude, latitude)

# 学区を特定
district = None
for index, school_district in school_districts.iterrows():
    if school_district['geometry'].contains(point):
        district = school_district
        break

# 学区内の小学校を取得
if district is not None:
    school_names = district['A27_006']+district['A27_007']
    print('通学する小学校:', school_names)
else:
    print('緯度経度が学区内にありません。')
