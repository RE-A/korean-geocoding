from korean_geocoding.geocoding import KoreanGeocoding as Kg

from assertpy import assert_that
import pickle


def test_find_coordinates_from_address():
    sample_addr1 = "서울특별시 종로구 종로2가"
    sample_addr1_coordinates = (126.9869027, 37.5704398)
    sample_addr2 = "충청북도 청주시 상당구 월오동"
    sample_addr2_coordinates = (127.5458, 36.6247071)

    kg = Kg()
    addr1_coord = kg.get_coordinates(sample_addr1)
    assert_that(addr1_coord).is_equal_to(sample_addr1_coordinates)
    addr2_coord = kg.get_coordinates(sample_addr2)
    assert_that(addr2_coord).is_equal_to(sample_addr2_coordinates)

def test_get_under_district():
    sample_addr1 = "서울특별시"
    sample_addr2 = "충청북도 음성군"

    kg = Kg()
    assert_that(len(kg.get_under_districts(sample_addr1))).is_equal_to(25)
    assert_that(len(kg.get_under_districts(sample_addr2))).is_equal_to(9)


