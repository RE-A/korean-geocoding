import pickle
from typing import Tuple, Optional
from korean_geocoding.section import Section
from korean_geocoding.sido_dict import SIDO_DICT
from pathlib import Path


class KoreanGeocoding:
    def __init__(self):
        self.geocode_data = dict()

    def _clean(self, sido_input):
        # TODO 약어를 사용한 시도를 찾을 수 있도록 (서울, 서울시 -> 서울특별시로 자동으로 인식) 함수 삽입 예정
        return sido_input

    def _load_geocode_data(self, sido_input: str):
        sido = sido_input  # _clean 함수 완성 시 교체 예정
        sido_filename = SIDO_DICT.get(sido)
        #
        if not sido_filename:
            raise ValueError("등록된 시도명이 아닙니다. 정식으로 등록된 시도명을 사용해 주세요.")

        fp = open(Path('..', 'data', f"{sido_filename}.dat"), 'rb')
        loaded_data = pickle.load(fp, encoding='utf-8')
        self.geocode_data[sido] = loaded_data

    def get_coordinates(self, query: str, delimiter=' ', just_fit=True) -> Tuple[Optional[float], Optional[float]]:
        # 입력한 좌표에 대한 위/경도 조회
        if not isinstance(query, str):
            raise ValueError("문자열 형태의 주소가 필요합니다.")

        section = self._search_section(query, delimiter, just_fit)
        return section.coordinates

    def _search_section(self, query: str, delimiter=' ', just_fit=True) -> Section:
        if not isinstance(query, str):
            raise ValueError("문자열 형태의 주소가 필요합니다.")

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
                    raise ValueError("해당 주소와 일치하는 행정구역이 없습니다")
                else:
                    return desired_section

        return desired_section

    def get_under_districts(self, query, delimiter=' ', just_fit=True) -> list:
        # 입력된 곳의 하위 행정구역 조회
        section = self._search_section(query, delimiter, just_fit)
        under_districts = []
        for child in section.children:
            under_districts.append(child.last_addr)
        return under_districts
