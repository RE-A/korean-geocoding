from pathlib import Path
import sys, json
import pickle
import time, requests

sys.path.append(Path('..'))

from korean_geocoding.section import Section
from korean_geocoding.sido_dict import SIDO_DICT

with open(Path("secret.json")) as fp:
    auth = json.load(fp)

API_URL = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
HEADERS = {"X-NCP-APIGW-API-KEY-ID": auth['NAVER_CLIENT_ID'],
           "X-NCP-APIGW-API-KEY": auth['NAVER_CLIENT_SECRET']}

def set_coordinate(section : Section):
    query = section.full_addr
    params = {'query': query.strip()}

    try:
        res=requests.get(API_URL, headers=HEADERS, params=params)
        res.raise_for_status()
    except Exception:
        return (None, None)

    content = res.json()

    if content['status'] != 'OK' or len(content['addresses']) == 0:
        return (None, None) # API 호출은 정상적으로 되었지만 API 서버 또는 쿼리 오류로 데이터가 없는 상태

    address_element = content['addresses'][0]
    latitude = float(address_element['y'])
    longitude = float(address_element['x'])
    section.coordinates = (longitude, latitude)

def set_coordinate_all(root_section):
    set_coordinate(root_section)
    time.sleep(0.5)
    for child in root_section.children.values():
        set_coordinate_all(child)

if __name__ == "__main__":
    import pprint
    pprint.pprint(set_coordinate(Section("", "충청북도")))







