from korean_geocoding.geocoding import KoreanGeocoding as Kg
import pytest
from assertpy import assert_that
import pickle


@pytest.fixture(scope="module")
def kg() -> Kg:
    kg = Kg()
    yield kg


def test_find_coordinates_from_address(kg):
    sample_addr1 = "서울특별시 종로구 종로2가"
    sample_addr1_coordinates = (37.5704398, 126.9869027)
    sample_addr2 = "충청북도 청주시 상당구 월오동"
    sample_addr2_wrong = "충청북도 청주시 상당구 이런곳없다동"
    sample_addr2_wrong_coordinates = (36.5897552, 127.5051229) # 충청북도 청주시 상당구
    sample_addr2_coordinates = (36.6247071, 127.5458)
    sample_addr3 = "서울특별시|종로구|종로2가"

    addr1_coord = kg.get_coordinates(sample_addr1)
    assert_that(addr1_coord).is_equal_to(sample_addr1_coordinates)
    addr2_coord = kg.get_coordinates(sample_addr2)
    assert_that(addr2_coord).is_equal_to(sample_addr2_coordinates)

    wrong_addr2_coord = kg.get_coordinates(sample_addr2_wrong, just_fit=False)
    assert_that(wrong_addr2_coord).is_equal_to(sample_addr2_wrong_coordinates)

    addr3_coord = kg.get_coordinates(sample_addr3, delimiter='|')
    assert_that(addr3_coord).is_equal_to(sample_addr1_coordinates)


def test_find_wrong_address(kg):
    wrong_address1 = "이름없는특별시 성동구 성수동"
    wrong_address2 = "경기도 성남시 중원구 존재하지않는동"

    with pytest.raises(ValueError):
        long_coord1 = kg.get_coordinates(wrong_address1)
    with pytest.raises(ValueError):
        long_coord2 = kg.get_coordinates(wrong_address2)

def test_get_under_district(kg):
    sample_addr1 = "서울특별시"
    sample_addr2 = "충청북도 음성군"
    sample_addr3 = "부산광역시 동구"

    assert_that(len(kg.get_under_districts(sample_addr1))).is_equal_to(25)
    assert_that(len(kg.get_under_districts(sample_addr2))).is_equal_to(9)
    assert_that(len(kg.get_under_districts(sample_addr3))).is_equal_to(15)

def test_get_distance(kg):
    sample_addr1 = "서울특별시 용산구 이태원동"
    sample_point1 = (37.5325225, 126.9950384) # 서울특별시 용산구 이태원동
    sample_addr2 = "서울특별시 중구 서소문동"
    sample_point2 = (37.563275, 126.973425) # 서울특별시 중구 서소문동

    assert_that(kg.get_distance(sample_addr1, sample_addr2)).is_equal_to(kg.get_distance(sample_addr1, sample_point2))
    assert_that(kg.get_distance(sample_addr1, sample_addr2)).is_equal_to(kg.get_distance(sample_point2, sample_point1))
    assert_that(kg.get_distance(sample_point1, sample_addr2)).is_equal_to(kg.get_distance(sample_addr1, sample_point2))
    assert_that(kg.get_distance(sample_point1, sample_addr1)).is_equal_to(0)
    assert_that(kg.get_distance((36.123142, 125.333213), "서울특별시 용산구 이태원동")).is_not_equal_to(0)



