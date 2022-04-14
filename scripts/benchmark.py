from timeit import timeit
from korean_geocoding.geocoding import KoreanGeocoding
from pathlib import Path
import json

with open(Path("secret.json")) as fp:
    auth = json.load(fp)

kg = KoreanGeocoding()
kg.set_naver_api(auth['NAVER_CLIENT_ID'], auth['NAVER_CLIENT_SECRET'])

testset = [
'부산광역시 동구 범일제5동',
'부산광역시 동구 범일제2동',
'부산광역시 동구 범일제1동',
'부산광역시 동구 좌천동',
'부산광역시 동구 수정제5동',
'전라남도 신안군 암태면 오상리',
'전라남도 신안군 암태면 단고리',
'전라남도 신안군 암태면 와촌리',
'충청남도 보령시 오천면 녹도리',
'충청남도 보령시 오천면 삽시도리',
'충청남도 보령시 오천면 원산도리',
'충청남도 보령시 오천면 효자도리',
]

def run_by_local_data():
    for data in testset:
        kg.get_coordinates(data)


def run_by_api():
    for data in testset:
        kg.get_coordinates_by_api(data)

print(timeit(run_by_local_data, number=1))
print(timeit(run_by_api, number=1))