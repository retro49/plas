# token type classifier
class TTC:
    __token_types = {
        0x000: "ERROR",
        0x001: "INSTRUCTION",
        0x002: "MEMORY",
        0x003: "VALUE",
        0x004: "LABEL",
        0x005: "SYMBOL",
        0x006: "ADDRESS"
    }

    @staticmethod
    def get_type(t: int) -> str:
        return TTC.__token_types[t]


class TokenType:
    TKN_INS = 0x01
    TKN_MEM = 0x02
    TKN_VAL = 0x03
    TKN_LBL = 0x04
    TKN_SYM = 0x05
    TKN_ADR = 0x06
    TKN_ERR = 0x00


class Token:
    def __init__(self):
        self.tokenType = None
        self.tokenData = None

    def set_type(self, token_type):
        self.tokenType = token_type

    def set_data(self, token_data):
        self.tokenData = token_data

    def get_type(self):
        return self.tokenType

    def get_data(self):
        return self.tokenData

    @classmethod
    def create_from(cls, token_type, token_data):
        token = Token()
        token.set_type(token_type)
        token.set_data(token_data)
        return token

    def __str__(self):
        return "<TYPE {0} ({1}), DATA {2}>".format(self.get_type(), TTC.get_type(self.get_type()), self.get_data())



