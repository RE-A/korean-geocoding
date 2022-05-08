from typing import Union, Optional
import requests


class Naver_Geocoding:
    API_URL = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"

    def __init__(self, client_id: str, client_secret: str):
        self.api_key: Optional[Union[str, str]] = None  # [KEY, SECRET_KEY] 형태
        self.HEADERS = {"X-NCP-APIGW-API-KEY-ID": client_id,
                        "X-NCP-APIGW-API-KEY": client_secret}

    def _check_resp_content(self, content: dict, query, ignore_empty):
        if content['meta']['totalCount'] == 0:
            # 데이터가 검색되지 않음
            if ignore_empty:
                return None
            else:
                raise ValueError(f"Cannot find any address result from the query '{query}'.")

        if content['meta']['totalCount'] > 1:
            # 여러 개의 데이터가 검색된 상태
            addr_candidates = [str((addr['roadAddress'], addr['y'], addr['x'])) for addr in content['addresses']]
            err_string = f"There are several addresses from your query '{query}', So we don't know which address should be selected. " \
                         f"Please give the more clear query.\n" \
                         f"Below is the result from your query.\n"
            candidates_str = '\n'.join(addr_candidates)
            err_string += candidates_str
            raise ValueError(err_string)

    def _parse_detail(self, contents: dict) -> dict:
        """
        :return:parse된 주소 오브젝트
        """
        #  0가지 or 2가지 이상 나오는 경우는 위에서 처리했음.
        result = dict()
        addr_content = contents.get('addresses')[0]
        result['road_address'] = addr_content['roadAddress']
        result['jibun_address'] = addr_content['jibunAddress']
        result['english_address'] = addr_content['englishAddress']

        result['address_elements'] = dict()
        result_addr_elems = result['address_elements']
        for elem in addr_content['addressElements']:
            typename = elem['types'][0]
            result_addr_elems[typename] = elem['longName']

        result['latitude'] = addr_content['y']
        result['longitude'] = addr_content['x']

        return result


    def req(self, query, ignore_empty, detailed) -> Union[Optional[tuple], dict]:
        if not self.HEADERS:
            raise ValueError("The authentication field is empty. "
                             "Please call Naver_Geocoding() instance first "
                             "with Naver Cloud Platform client-id and client-secret key.")

        params = {'query': query}
        try:
            resp = requests.get(self.API_URL, headers=self.HEADERS, params=params)
        except Exception as e:
            raise ConnectionError("Connection failed in sending request to NCP API Server.  "
                                  "Detailed error is blow:\n "
                                  f"{e}")
        if not resp.ok:
            err_msg = resp.json()['error']
            raise ConnectionError(f"{err_msg['message']}, {err_msg['details']} errCode: {err_msg['errorCode']}\n"
                                  "Read https://api.ncloud-docs.com/docs/ai-naver-mapsgeocoding for detailed information.")

        content = resp.json()
        self._check_resp_content(content, query, ignore_empty)

        if detailed:
            return self._parse_detail(content)

        coord = content['addresses'][0]
        return float(coord['y']), float(coord['x'])


if __name__ == "__main__":
    # For Live Test
    import json, pprint
    from pathlib import Path

    with open(Path('..', 'scripts', 'secret.json'), 'r') as fp:
        auth = json.load(fp)
    ng = Naver_Geocoding(auth['NAVER_CLIENT_ID'], auth['NAVER_CLIENT_SECRET'])
    pprint.pprint(ng.req("서울특별시 용산구 한강대로 366", detailed=True, ignore_empty=False))
