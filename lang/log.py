import sys


class Log:
    """ logging class """
    __GREEN = '\033[1;32m'
    __NORM = '\033[0;00m'
    __RED = '033[1;31m'

    """ debugging purpose """
    @staticmethod
    def d(key: str, message: str):
        sys.stdout.write(
            Log.__GREEN + str(key) +
            str(": ") +
            Log.__NORM +
            str(message) +
            chr(0x0a)
        )

    """ error mode """
    @staticmethod
    def e(key: str, message: str):
        sys.stdout.write(
            Log.__RED + str(key) + str(": ") +
            Log.__NORM +
            str(message) +
            chr(0x0a)
        )

    """ normal writer """
    @staticmethod
    def w(message: str):
        sys.stdout.write(Log.__NORM + str(message) + chr(0x0a))
