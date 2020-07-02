from json import JSONEncoder
from model.response import Response
import json


class ResponseEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(object, Response):
            return object.__dict__
        else:
            return json.JSONEncoder.default(self, o)
