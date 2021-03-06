import openpyxl
from pathlib import Path
import sys
import pickle

sys.path.append(Path('..'))

from korean_geocoding.section import Section
from korean_geocoding.common import SIDO_DICT
from scripts.set_coordinate import set_coordinate_all


def extract_data(target_sido):
    """
    각 시도별로 데이터 추출 후 저장
    """

    document = openpyxl.load_workbook(Path('original_coordinate.xlsx'), read_only=True)
    sheet = document['합본 DB']

    # 최초 초기화
    region_data = Section('', target_sido)
    region_data.full_addr = region_data.full_addr.strip()

    for row in sheet.iter_rows(min_row=2):
        sido = row[1].value
        if sido != target_sido:
            continue
        if row[2].value and (' ' in row[2].value):
            sigun, gu = row[2].value.split()
        else:
            sigun, gu = row[2].value, ''
        dong = row[3].value
        li = row[4].value

        sections = [section for section in (sigun, gu, dong, li) if section]
        Section.add_child(region_data, sections)

    return region_data


if __name__ == "__main__":
    for sido in SIDO_DICT:
        data = extract_data(sido)
        set_coordinate_all(data)
        import pprint
        pprint.pprint(Section.get_address_full_list(data))
        fp = open(Path('..', 'data', f"{SIDO_DICT[sido]}.dat"), 'wb')
        pickle.dump(data, fp)
        fp.close()