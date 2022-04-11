class Section:

    def __init__(self, addr: str, last_addr: str):
        self.children = dict()
        self.last_addr = last_addr
        self.full_addr = addr + ' ' + last_addr
        self.coordinates = None  # (위도, 경도)

    @staticmethod
    def add_child(root_section, child_sections: list):
        if not child_sections:
            return
        now = child_sections[0]
        if now not in root_section.children:
            root_section.children[now] = Section(root_section.full_addr, now)
        Section.add_child(root_section.children[now], child_sections[1:])

    @staticmethod
    def _get_addr_tree(root_section, addrlist):
        addrlist.append(str(root_section))
        for child in root_section.children.values():
            Section._get_addr_tree(child, addrlist)

    @staticmethod
    def get_address_full_list(root_section):
        full_addr_list = []
        Section._get_addr_tree(root_section, full_addr_list)
        return full_addr_list

    def __str__(self):
        return self.full_addr + f" {self.coordinates if self.coordinates else ''}"
