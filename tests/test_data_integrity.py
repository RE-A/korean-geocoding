from korean_geocoding.section import Section
from korean_geocoding.sido_dict import SIDO_DICT

from pathlib import Path
from assertpy import assert_that
import pickle

def test_seoul_data_can_load_successfully():
    SEOUL_COUNT_OF_GU = 25
    SEOUL_CITY_HALL_COORIDATES = ()

    with open(Path('..','data','Seoul.dat'), 'rb') as fp:
        seoul_data: Section = pickle.load(fp)
    assert_that(len(Section.get_address_full_list(seoul_data))).is_greater_than(800) # 약 800개
    assert_that(len(seoul_data.children)).is_equal_to(SEOUL_COUNT_OF_GU)
    assert_that(seoul_data.coordinates).is_equal_to((126.9783882, 37.5666103))

def test_other_area_data_can_load():
    for sido in SIDO_DICT:
        filename = SIDO_DICT[sido] + '.dat'
        with open(Path('..', 'data', filename), 'rb') as fp:
            area_data: Section = pickle.load(fp)
            assert_that(area_data).is_instance_of(Section)
            assert_that(len(area_data.children)).is_greater_than(0)
            assert_that(area_data.coordinates).is_not_equal_to((None, None))











