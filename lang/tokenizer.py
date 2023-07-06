import re
from .token_unit import TokenType
from .token_unit import Token
from .util import ASCIIHelper


class TokenMatcher:
    def __init__(self, token):
        self.__ins_regex = r"(putc|load|go|exit|eval|ifeq|ifne|ifgt|iflt|ifge|ifle|add|sub|mul|idiv|div|home|log|data)"
        self.__mem_regex = r"\$([0-9]|[a-f])"
        self.__val_regex = r'\-?([0-9]+|[0-9]*)\.?([0-9]*|[0-9]+)'
        self.__lbl_regex = r"[a-zA-Z_]+[a-zA-Z0-9_]*"
        self.__sym_regex = ASCIIHelper.SYM_REGEX

        self.token = token
        self.tkn = Token()
        self.tkn.set_data(self.token)

    def get_token_type(self):
        if re.fullmatch(self.__ins_regex, self.token):
            self.tkn.set_type(TokenType.TKN_INS)
        elif re.fullmatch(self.__mem_regex, self.token):
            self.tkn.set_type(TokenType.TKN_MEM)
        elif re.fullmatch(self.__val_regex, self.token):
            self.tkn.set_type(TokenType.TKN_VAL)
        elif re.fullmatch(self.__lbl_regex, self.token):
            self.tkn.set_type(TokenType.TKN_LBL)
        elif re.fullmatch(self.__sym_regex, self.token):
            self.tkn.set_type(TokenType.TKN_SYM)
        else:
            self.tkn.set_type(TokenType.TKN_ERR)

        return self.tkn


class Tokenizer:
    def __init__(self, source_stream):
        self.ss = source_stream
        self.codes = []
        self.lines = []
        self.tokens = {}
        for __ss in self.ss:
            self.codes.append(__ss[0])
            self.lines.append(__ss[1])

        self.__tokenize()

    def to_file(self, file):
        data = ""
        if len(self.tokens.keys()) == 0:
            return
        large_line = len(str(max(self.tokens.keys())))
        for (line, line_tokens) in self.tokens.items():
            line_data = ""
            token_data = ""
            for token in line_tokens:
                line_data += str(token.get_data()) + " "
                token_data += str(token)
            _line = "%{0}d: %-20s | %5s\n".format(large_line)
            _line = _line % (line, line_data, token_data)
            # line = "%5d: %-20s | %5s\n" % (line, line_data, token_data)
            data += _line

        with open(file, "w+") as f:
            f.write(data)

    def get_tokens(self):
        return self.tokens

    def __tokenize(self):
        lp = 0
        for code in self.codes:
            formatted_code = Tokenizer.__pas_formatter(code)
            fcl = []
            for fc in formatted_code:
                fcl.append(TokenMatcher(fc).get_token_type())

            self.tokens[self.lines[lp]] = fcl
            lp += 1

    @staticmethod
    def __pas_formatter(code: str) -> list:
        formatted = []
        data = ""
        for char in code:
            if ASCIIHelper.is_alphanum(char):
                data += char
            else:
                if char == '_' or char == '$' or char == '-' or char == '.':
                    data += char
                elif char == ' ':
                    if data == "":
                        continue
                    else:
                        formatted.append(data)
                        data = ""
                else:
                    if data == "":
                        formatted.append(char)
                    else:
                        formatted.append(data)
                        formatted.append(char)
                        data = ""
        if not data == "":
            formatted.append(data)

        return formatted
