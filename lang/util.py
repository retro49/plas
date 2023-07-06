import re
import os
import sys


class SourceStream:
    """ reads a source code file """

    def __init__(self, file: str):
        self.file = file
        # check file
        if not os.path.exists(self.file):
            sys.stdout.write("source stream not found\n")
            return

        self.stream = ""
        self.__read_stream()

    def __read_stream(self):
        with open(self.file, "r") as f:
            self.stream += f.read()

    def get_stream(self) -> str:
        """ returns the source code stream """
        return self.stream

    def __str__(self) -> str:
        return self.stream


class ASCIIHelper:
    """ ascii helper functions """
    ALPHA_REGEX = r"[a-zA-Z]"
    ALPHANUM_REGEX = r"[a-zA-Z0-9]"
    NUM_REGEX = r"[0-9]+"
    SYM_REGEX = r"[^a-zA-Z0-9]"

    @staticmethod
    def is_alpha(c: chr) -> bool:
        """ checks if c is a alphabet character """
        if re.fullmatch(ASCIIHelper.ALPHA_REGEX, c):
            return True

        return False

    @staticmethod
    def is_alphanum(c: chr) -> bool:
        """ checks if c is either an alphabet or number """
        if re.fullmatch(ASCIIHelper.ALPHANUM_REGEX, c):
            return True

        return False

    @staticmethod
    def is_num(c: chr) -> bool:
        """ checks if c is a numeric character """
        if re.fullmatch(ASCIIHelper.NUM_REGEX, c):
            return True

        return False

    @staticmethod
    def is_special_char(c: chr) -> bool:
        """ checks if c is a spacial character """
        if re.fullmatch(ASCIIHelper.SYM_REGEX, c):
            return True

        return False
