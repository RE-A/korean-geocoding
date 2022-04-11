# 전체 데이터에 대해 어떤 작업을 해야 할때 사용하는 스크립트
import collections
from korean_geocoding.section import Section
from korean_geocoding.sido_dict import SIDO_DICT
import pickle
from pathlib import Path


for sido in SIDO_DICT:
    with open(Path('..', 'korean_geocoding', 'data', f'{SIDO_DICT[sido]}.dat'), 'rb') as fp:
        root_section: Section = pickle.load(fp)
    stack = collections.deque()
    stack.append(root_section)

    while stack:
        section = stack.popleft()
        # 필요한 로직을 아래에 작성
        for child in list(section.children.keys()):
            if child.endswith('출장소'):
                del(section.children[child])

        for child in section.children.values():
            stack.appendleft(child)
        # if section.coordinates:
        #     section.coordinates = (section.coordinates[1], section.coordinates[0])

    # 처리 후 다시 저장
    with open(Path('..', 'korean_geocoding', 'data', f'{SIDO_DICT[sido]}.dat'), 'wb') as fp:
        pickle.dump(root_section, fp)










