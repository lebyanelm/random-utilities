# dependencies
import nanoid
import json
import bson
import os
from random_utilities.models.time_created import TimeCreatedModel

class DataModel:
    def __init__(self):
        self.key = nanoid.generate()
        self.time_created = TimeCreatedModel().__dict__
        self.last_modified = TimeCreatedModel().__dict__
        self._selected_database_ = "live" if os.environ.get("ENVIRONMENT") == "production" else "testing"

    def to_json(self) -> str:            
        return json.dumps(obj=self.__dict__)

    def to_dict(self) -> dict:
        new_self_dict = {**self.__dict__}
        return self._obj_to_dict(new_self_dict)

    @classmethod
    def _obj_to_dict(cls, obj):
        if type(obj) == dict:
            for parameter in obj:
                if type(obj[parameter]) == dict:
                    obj[parameter] = cls._obj_to_dict(obj[parameter])
                else:
                    allowed_objects = [str, bool, int, float, type(None)]
                    if type(obj[parameter]) == list:
                        obj[parameter] = cls._obj_to_dict(obj[parameter])
                    elif type(obj[parameter]) not in allowed_objects:
                        obj[parameter] = str(obj[parameter])
        elif type(obj) == list:
            for index, _ in enumerate(obj):
                if type(obj[index]) == bson.objectid.ObjectId:
                    obj[index] = str(obj[index])
                else:
                    obj[index] = cls._obj_to_dict(obj[index])
        return obj

    def get_schema():
        return { }

    @classmethod
    def verify_schema(cls, data: dict, schema = None) -> list:
        schema = schema if schema is not None else cls.get_schema()
        schema_keys = schema.keys()
        errors = []
        for schema_key in schema_keys:
            if data.get(schema_key):
                # If the schema contains multiple datatypes
                if type(schema[schema_key]) in (list, tuple):
                    if data.get(schema_key) not in schema[schema_key]:
                        errors.append({ "error": f'Invalid data type "{type(data.get(schema_key)).__name__}" used in {schema_key}. "{schema[schema_key]}" required instead.', "error_type": "invalid"})
                else:
                    if type(data.get(schema_key)) != schema[schema_key]:
                        errors.append({ "error": f'Invalid data type "{type(data.get(schema_key)).__name__}" used in {schema_key}. "{schema[schema_key].__name__}" required instead.', "error_type": "invalid"})
            else:
                errors.append({ "error": f"Attribute {schema_key} of {type(schema[schema_key]).__name__} required in request body.", "error_type": "undefined" })
        return errors