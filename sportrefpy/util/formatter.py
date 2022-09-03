import json
from typing import Union

from pandas import DataFrame
from pandas import Series


class Formatter:
    @staticmethod
    def return_dict_or_json(pd: Union[DataFrame, Series], fmt: str):
        if fmt == "json":
            return json.dumps(pd.transpose().to_dict())
        return pd.transpose().to_dict()
