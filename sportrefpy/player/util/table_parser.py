from typing import List

from bs4 import BeautifulSoup


class TableParser:
    @staticmethod
    def parse_table_ids(soup: BeautifulSoup, class_name: str):
        tables = soup.find_all("table", {"class": class_name})
        return [t["id"] for t in tables]

    @staticmethod
    def parse_attr_id(table_ids: List[str], id_names: List[str]):
        for t_id in table_ids:
            if t_id in id_names:
                return t_id
        return None
