"""
참고:
https://yganalyst.github.io/spatial_analysis/spatial_analysis_3/
좌표계 관련해서는 내용이 방대하므로, 딱 필요한 부분만 구현

epsg:4326이 흔히 아는 위경도 좌표
epsg:3857 : 네이버 지도에서 사용하는 좌표
epsg:5184/ 5189 : 국가 API에서 주로 사용하는 좌표
"""

from typing import Optional, Tuple
from pyproj import Transformer


class Converter:
    def __init__(self, from_crs: str, to_crs: str="epsg:4326" ):
        # from_crs : 'epsg:xxxx' 형태
        self.tranformer: Optional[Transformer] = None
        self.set_converter(from_crs, to_crs)

    def set_converter(self, from_crs: str, to_crs: str = "epsg:4326"):
        self.tranformer = Transformer.from_crs(from_crs, to_crs)

    def convert(self, from_coord: Tuple[float, float]):
        return self.tranformer.transform(from_coord[0], from_coord[1])

    def smart_inference(self):
        raise NotImplementedError

if __name__ == "__main__":
    # For live test in coding
    con = Converter("epsg:3857")
    print(con.convert((14091746.0092059,4084906.3085543)))
