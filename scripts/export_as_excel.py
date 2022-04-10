import openpyxl
import collections
from korean_geocoding.section import Section
from korean_geocoding.sido_dict import SIDO_DICT
import pickle
from pathlib import Path

wb = openpyxl.Workbook()
wb_filename = "행정구역별_위경도_좌표.xlsx"


for sido in SIDO_DICT:
    ws = wb.create_sheet(title=sido)
    ws.append(['시도', '시군구', '읍면동/구', '읍/면/리/동', '리', '위도', '경도'])
    with open(Path('..', 'korean_geocoding', 'data', f'{SIDO_DICT[sido]}.dat'), 'rb') as fp:
        root_section: Section = pickle.load(fp)
    stack = collections.deque()
    stack.append(root_section)

    while stack:
        row = ['']*7
        section = stack.popleft()
        for child in section.children.values():
            stack.appendleft(child)
        district_names = section.full_addr.split()
        assert len(district_names) < 6
        for i, name in enumerate(district_names):
            row[i] = name
        if section.coordinates:
            row[5], row[6] = section.coordinates

        ws.append(row)

wb.save(wb_filename)









