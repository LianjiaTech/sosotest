import requests

class TypeTool(object):
    @staticmethod
    def is_bool(objData):
        if type(objData) == type(True):
            return True
        else:
            return False

    @staticmethod
    def is_bytes(objData):
        if type(b'') == type(objData):
            return True
        else:
            return False

    @staticmethod
    def is_str(objData):
        if type("") == type(objData):
            return True
        else:
            return False

    @staticmethod
    def is_dict(objData):
        if type({}) == type(objData):
            return True
        else:
            return False

    @staticmethod
    def is_list(objData):
        if type([]) == type(objData):
            return True
        else:
            return False

    @staticmethod
    def is_int(objData):
        if type(1) == type(objData):
            return True
        else:
            return False

    @staticmethod
    def is_float(objData):
        if type(1.1) == type(objData):
            return True
        else:
            return False

    @staticmethod
    def is_requests_Response(objData):
        if type(requests.models.Response()) == type(objData):
            return True
        else:
            return False

    @staticmethod
    def is_ValueError(objData):
        if type(ValueError("")) == type(objData):
            return True
        else:
            return False

    @staticmethod
    def is_requests_session(objData):
        if type(requests.session()) == type(objData):
            return True
        else:
            return False



