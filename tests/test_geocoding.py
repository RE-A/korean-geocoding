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
    sample_addr1_abb = "서울시 종로구 종로2가"
    sample_addr1_coordinates = (37.5704398, 126.9869027)
    sample_addr2 = "충청북도 청주시 상당구 월오동"
    sample_addr2_wrong = "충청북도 청주시 상당구 이런곳없다동"
    sample_addr2_wrong_coordinates = (36.5897552, 127.5051229)  # 충청북도 청주시 상당구
    sample_addr2_coordinates = (36.6247071, 127.5458)
    sample_addr3 = "서울특별시|종로구|종로2가"

    addr1_coord = kg.get_coordinates(sample_addr1)
    assert_that(addr1_coord).is_equal_to(sample_addr1_coordinates)
    addr1_abb_coord = kg.get_coordinates(sample_addr1_abb)
    assert_that(addr1_abb_coord).is_equal_to(sample_addr1_coordinates)
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
        wrong_coord1 = kg.get_coordinates(wrong_address1)
    with pytest.raises(ValueError):
        wrong_coord2 = kg.get_coordinates(wrong_address2)


def test_get_under_district(kg):
    sample_addr1 = "서울특별시"
    sample_addr2 = "충청북도 음성군"
    sample_addr3 = "부산광역시 동구"
    sample_addr4 = "충북 청주시"
    sample_addr5 = "충북 청주시 상당구"

    assert_that(len(kg.get_under_districts(sample_addr1))).is_equal_to(25)
    assert_that(len(kg.get_under_districts(sample_addr2))).is_equal_to(9)
    assert_that(len(kg.get_under_districts(sample_addr3))).is_equal_to(15)
    assert_that(len(kg.get_under_districts(sample_addr4))).is_equal_to(4)
    assert_that(len(kg.get_under_districts(sample_addr5))).is_equal_to(37)


def test_get_distance(kg):
    sample_addr1 = "서울특별시 용산구 이태원동"
    sample_point1 = (37.5325225, 126.9950384)  # 서울특별시 용산구 이태원동
    sample_addr2 = "서울특별시 중구 서소문동"
    sample_point2 = (37.563275, 126.973425)  # 서울특별시 중구 서소문동

    assert_that(kg.get_distance(sample_addr1, sample_addr2)).is_equal_to(kg.get_distance(sample_addr1, sample_point2))
    assert_that(kg.get_distance(sample_addr1, sample_addr2)).is_equal_to(kg.get_distance(sample_point2, sample_point1))
    assert_that(kg.get_distance(sample_point1, sample_addr2)).is_equal_to(kg.get_distance(sample_addr1, sample_point2))
    assert_that(kg.get_distance(sample_point1, sample_addr1)).is_equal_to(0)
    assert_that(kg.get_distance((36.123142, 125.333213), "서울특별시 용산구 이태원동")).is_not_equal_to(0)


def test_naver_api(kg):
    # 실제로 네이버 API를 날린 후 확인하는 건 테스트 세팅이나 성공여부 확인 등 여러 가지 외부적 문제가 생기므로 항상 온다고 가정.
    # 아래 데이터는 실제 데이터와 관련 없음.
    # TODO API 서버 모킹해서 response 받는 부분도 테스트 가능하도록 하기
    resp_sample1 = {'status': 'OK',
                    'meta': {'totalCount': 1, 'page': 1, 'count': 1},
                    'addresses': [{'roadAddress': '서울특별시 용산구 새창로 45길 3',
                                   'jibunAddress': '서울특별시 용산구 새창로 45길 3',
                                   'x': '126.973425',
                                   'y': '37.563275',
                                   'distance': 0.0}],
                    'errorMessage': ''}
    resp_sample2 = {'status': 'OK',
                    'meta': {'totalCount': 2, 'page': 1, 'count': 2},
                    'addresses': [{'roadAddress': '서울특별시 용산구 새창로 45길 3',
                                   'jibunAddress': '서울특별시 용산구 새창로 45길 3',
                                   'x': '126.973425',
                                   'y': '37.563275',
                                   'distance': 0.0},
                                  {'roadAddress': '서울특별시 용산구 새창로 45길 31',
                                   'jibunAddress': '서울특별시 용산구 새창로 45길 31',
                                   'x': '126.9735',
                                   'y': '37.5635',
                                   'distance': 0.0}],
                    'errorMessage': ''}
    resp_sample3 = {'status': 'OK',
                    'meta': {'totalCount': 0, 'page': 1, 'count': 0},
                    'addresses': []}

    kg.set_naver_api('1234', '123444')  # 실제로 요청을 보내지 않으므로 했다고 가정
    assert_that(kg.naver_api.HEADERS['X-NCP-APIGW-API-KEY-ID']).is_equal_to('1234')
    assert_that(kg.naver_api.HEADERS['X-NCP-APIGW-API-KEY']).is_equal_to('123444')

    assert_that(kg.naver_api._check_resp_content(resp_sample1, '쿼리', False)).is_none()  # 에러 없이 정상 통과
    with pytest.raises(ValueError, match="There are several addresses"):
        kg.naver_api._check_resp_content(resp_sample2, '쿼리', False)
    with pytest.raises(ValueError, match="Cannot find any address"):
        kg.naver_api._check_resp_content(resp_sample3, '쿼리', False)


def test_parse_detail_naver_api_result(kg):
    resp_sample = {'status': 'OK', 'meta': {'totalCount': 1, 'page': 1, 'count': 1},
                   'addresses': [{'roadAddress': '서울특별시 용산구 한강대로 366 트윈시티 남산',
                                  'jibunAddress': '서울특별시 용산구 동자동 56 트윈시티 남산',
                                  'englishAddress': "366, Hangang-daero, Yongsan-gu, Seoul, Republic of Korea",
                                  'addressElements': [{'types': ['SIDO'], 'longName': '서울특별시', 'shortName': '서울특별시', 'code': ''},
                                                      {'types': ['SIGUGUN'], 'longName': '용산구', 'shortName': '용산구', 'code': ''},
                                                      {'types': ['DONGMYUN'], 'longName': '동자동', 'shortName': '동자동', 'code': ''},
                                                      {'types': ['RI'], 'longName': '', 'shortName': '', 'code': ''},
                                                      {'types': ['ROAD_NAME'], 'longName': '한강대로', 'shortName': '한강대로', 'code': ''},
                                                      {'types': ['BUILDING_NUMBER'], 'longName': '366', 'shortName': '366', 'code': ''},
                                                      {'types': ['BUILDING_NAME'], 'longName': '트윈시티 남산', 'shortName': '트윈시티 남산', 'code': ''},
                                                      {'types': ['LAND_NUMBER'], 'longName': '56', 'shortName': '56', 'code': ''},
                                                      {'types': ['POSTAL_CODE'], 'longName': '04323', 'shortName': '04323', 'code': ''}],
                                  'x': '126.9729133',
                                  'y': '37.5511247', 'distance': 0.0}], 'errorMessage': ''}
    kg.set_naver_api('1234', '123444')  # 실제로 요청을 보내지 않으므로 했다고 가정

    parsed_data = kg.naver_api._parse_detail(resp_sample)

    assert_that(parsed_data).contains('english_address', 'road_address', 'jibun_address', 'address_elements', 'latitude', 'longitude')
    assert_that(parsed_data.get('address_elements')).contains('BUILDING_NAME', 'BUILDING_NUMBER', 'DONGMYUN', 'LAND_NUMBER', 'POSTAL_CODE',
                                                              'RI', 'ROAD_NAME', 'SIDO', 'SIGUGUN')



def test_coordinates_convert(kg):
    coord_WGS84 = (37.56, 126.97)  # 위경도 좌표
    coord_3857 = (14133857.26, 4517734.55)
    coord_5174 = (451391.18, 196794.06)

    # 좌표계 설정하지 않은 상태
    with pytest.raises(ValueError):
        kg.convert(coord_3857)

    kg.set_converter("epsg:3857")
    lat, long = kg.convert(coord_3857)
    assert_that(coord_WGS84[0]).is_equal_to(pytest.approx(lat, abs=0.01))
    assert_that(coord_WGS84[1]).is_equal_to(pytest.approx(long, abs=0.01))

    kg.set_converter("epsg:5174")
    lat, long = kg.convert(coord_5174)
    # 블로그에 아래 approx 사용법 정리하기
    assert_that(coord_WGS84[0]).is_equal_to(pytest.approx(lat, abs=0.01))
    assert_that(coord_WGS84[1]).is_equal_to(pytest.approx(long, abs=0.01))
