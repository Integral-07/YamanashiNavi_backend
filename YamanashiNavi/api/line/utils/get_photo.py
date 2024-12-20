import googlemaps, os

# Google Maps APIキー
API_KEY = os.getenv('GOOGLE_MAPS_API')

# Google Mapsクライアントを作成
gmaps = googlemaps.Client(key=API_KEY)

def get_place_photo(place_name):#, location, radius=1000):
    """
    指定した場所の施設画像を取得する
    :param place_name: 検索する施設名
    :param location: 検索の中心地点 (緯度, 経度) 例: "35.6895,139.6917"
    :param radius: 検索範囲 (メートル)
    :return: 画像URL
    """
    # 1. Place Search APIを使用して施設を検索
    places_result = gmaps.places(
        query=place_name,
        #location=location,
        #radius=radius
    )

    if not places_result.get('results'):
        return "施設が見つかりませんでした"

    # 最初の施設を取得
    place = places_result['results'][0]
    place_id = place['place_id']
    print(f"施設名: {place['name']}")
    print(f"住所: {place.get('formatted_address')}")

    # 2. Place Details APIで写真情報を取得
    place_details = gmaps.place(place_id=place_id)

    if 'photos' not in place_details['result']:
        return None

    # 3. Place Photos APIを使用して画像を取得
    photo_reference = place_details['result']['photos'][0]['photo_reference']
    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}"

    return photo_url
