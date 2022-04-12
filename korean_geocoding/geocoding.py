import pickle
from typing import Tuple, Union, Optional
from korean_geocoding.section import Section
from korean_geocoding.sido_dict import SIDO_DICT
from korean_geocoding.NG_API import Naver_Geocoding
from haversine import haversine
from pathlib import Path

class KoreanGeocoding:
    def __init__(self):
        self.geocode_data = dict()
        self._current_path = Path(__file__).parent.resolve()
        self.naver_api: Optional[Naver_Geocoding] = None

    def _clean(self, sido_input):
        # TODO 약어를 사용한 시도를 찾을 수 있도록 (서울, 서울시 -> 서울특별시로 자동으로 인식) 함수 삽입 예정
        return sido_input

    def _load_geocode_data(self, sido_input: str):
        sido = sido_input  # _clean 함수 완성 시 교체 예정
        sido_filename = SIDO_DICT.get(sido)

        if not sido_filename:
            raise ValueError(f"Cannot recognize district name '{sido_input}'.")
        fp = open(Path(self._current_path, 'data', f"{sido_filename}.dat"), 'rb')
        loaded_data = pickle.load(fp, encoding='utf-8')
        fp.close()
        self.geocode_data[sido] = loaded_data

    def _search_section(self, query: str, delimiter=' ', just_fit=True) -> Section:
        if not isinstance(query, str):
            raise ValueError(f"'{query}' is not a string.")

        splited_query = query.split(delimiter)
        desired_section = self.geocode_data
        sido = splited_query[0]
        if sido not in desired_section:
            self._load_geocode_data(sido)

        desired_section = self.geocode_data[sido]

        for section in splited_query[1:]:
            if section in desired_section.children:
                desired_section = desired_section.children[section]
            else:
                # 매치되지 않는 쿼리문이 남은 상태
                if just_fit:
                    raise ValueError(f"The query '{query}' doesn't match any of the district name.")
                else:
                    return desired_section

        return desired_section

    def set_naver_api(self, client_id, client_secret):
        # 네이버 API 사용을 위한 세팅
        self.naver_api = Naver_Geocoding(client_id, client_secret)

    def get_coordinates_by_api(self, query: str, delimiter=' ', ignore_empty=False, detailed=False):
        # TODO : self.naver_api 체크하는 부분 데코레이터로 만들 수 있을 것 같음.
        if not self.naver_api:
            raise ValueError("Please call set_naver_api() first and set the NCP client keys.")

        if delimiter != ' ':
            query = query.replace(delimiter, ' ')

        return self.naver_api.req(query, ignore_empty, detailed)

    def get_coordinates(self, query: str, delimiter=' ', just_fit=True) -> Tuple[float, float]:
        # 입력한 좌표에 대한 위/경도 조회
        if not isinstance(query, str):
            raise ValueError(f"'{query}' is not a string.")

        section = self._search_section(query, delimiter, just_fit)
        return section.coordinates

    def get_under_districts(self, query, delimiter=' ', just_fit=True) -> list:
        # 입력된 곳의 하위 행정구역 조회
        section = self._search_section(query, delimiter, just_fit)
        under_districts = []
        for child in section.children.values():
            under_districts.append(child.last_addr)
        return under_districts

    def get_distance(self, query1: Union[str, Tuple[float, float]], query2: Union[str, Tuple[float, float]],
                     delimiter=' ', just_fit=True) -> float:
        point1 = query1 # Tuple일시
        if isinstance(query1, str):
            point1 = self.get_coordinates(query1, delimiter, just_fit)

        point2 = query2  # Tuple일시
        if isinstance(query2, str):
            point2 = self.get_coordinates(query2, delimiter, just_fit)

        return round(haversine(point1, point2), 3)
