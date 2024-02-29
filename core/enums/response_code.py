from enum import IntEnum


class ResponseCode(IntEnum):
    def __new__(cls, value, phrase, response=""):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.phrase = phrase
        obj.response = response
        return obj

    @classmethod
    def phrase(ob):
        return ob.phras

    def as_response_item(self, append: dict = {}):
        serializable = {"code": self.value, "message": self.phrase}
        serializable.update(append)
        return serializable

    success = 1001, "success"
    does_not_match = 101, "does not match"
