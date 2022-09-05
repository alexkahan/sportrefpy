import json
from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Union

from pandas import DataFrame
from pandas import Series


class Formatter(ABC):
    @staticmethod
    def convert(data: Union[DataFrame, Series, Dict], fmt: str):
        if fmt == "json":
            return JSONFormatter().output(data)
        elif fmt == "pandas":
            return PandasFormatter().output(data)
        elif fmt == "dict":
            return DictFormatter().output(data)

    @staticmethod
    def clean_player_name(player: str):
        return player.split("(")[0].strip("+* ")

    @staticmethod
    @abstractmethod
    def output(data):
        raise NotImplementedError


class JSONFormatter(Formatter):
    @staticmethod
    def output(data):
        return json.dumps(data)


class DictFormatter(Formatter):
    @staticmethod
    def output(data):
        if isinstance(data, dict):
            return data
        if isinstance(data, (DataFrame, Series)):
            return data.transpose().to_dict()


class PandasFormatter(Formatter):
    @staticmethod
    def output(data):
        if isinstance(data, (DataFrame, Series)):
            return data
