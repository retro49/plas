#!/bin/python3
import sys
import os
import re

"""
@author: Naol Dereje
@data: 21/10/2022
Pretend Like Assembly (plas)
A simple assembly like programming language prototype. Test for how a compiler works.
There are only 16 registers in plas until add memory access but not in this language tho.
Anyways by using these 16 registers namely known as $0 - $f in hexadecimal representation
we can store any kind of numbers except strings. Instructions are executed line by line.
so you can have the instructions from INSTRUCTION_ID class.
"""


# PAS instructions
class INSTRUCTION_ID:
    PUTC = 0X001
    LOAD = 0X002
    GO = 0X003
    EXIT = 0X004
    EVAL = 0X005
    IFEQ = 0X006
    IFNE = 0X007
    IFGT = 0X008
    IFLT = 0X009
    IFGE = 0X00A
    IFLE = 0X00B
    ADD = 0X00C
    SUB = 0X00D
    MUL = 0X00E
    IDIV = 0X00F
    DIV = 0x010
    HOME = 0x011
    LOG = 0x012
    DATA = 0x013


# for now there is no support for floating point 
# operations but for later i will be implementing a
# floating point memory and operations on them
# instruction table for accessing instantly
class InstructionTable:
    INS = {
        "putc": INSTRUCTION_ID.PUTC,
        "load": INSTRUCTION_ID.LOAD,
        "go": INSTRUCTION_ID.GO,
        "exit": INSTRUCTION_ID.EXIT,
        "eval": INSTRUCTION_ID.EVAL,
        "ifeq": INSTRUCTION_ID.IFEQ,
        "ifne": INSTRUCTION_ID.IFNE,
        "ifgt": INSTRUCTION_ID.IFGT,
        "iflt": INSTRUCTION_ID.IFLT,
        "ifge": INSTRUCTION_ID.IFGE,
        "ifle": INSTRUCTION_ID.IFLE,
        "add": INSTRUCTION_ID.ADD,
        "sub": INSTRUCTION_ID.SUB,
        "mul": INSTRUCTION_ID.MUL,
        "idiv": INSTRUCTION_ID.IDIV,
        "div": INSTRUCTION_ID.DIV,
        "home": INSTRUCTION_ID.HOME,
        "log": INSTRUCTION_ID.LOG,
        "data": INSTRUCTION_ID.DATA
    }


# __memory address table found in pas
class FMT:
    flags = {
        0x00: "feq",
        0x01: "fne",
        0x02: "fgt",
        0x03: "flt",
        0x04: "fge",
        0x05: "fle"
    }
    FEQ = 0  # flag equal index
    FNE = 1  # flag not equal index
    FGT = 2  # flag greater than index
    FLT = 3  # flag less than index
    FGE = 4  # flag greater than or equal index
    FLE = 5  # flag less than or equal index


# an object for storing flags
# used after evaluation process
class FlagMemory:
    def __init__(self):
        self.feq = False
        self.fne = False
        self.fgt = False
        self.flt = False
        self.fge = False
        self.fle = False
        self.__fmem = {
            "feq": False,
            "fne": False,
            "fgt": False,
            "flt": False,
            "fge": False,
            "fle": False
        }

    def enable_flag(self, flag):
        self.__fmem[flag] = True

    def disable_flag(self, flag):
        self.__fmem[flag] = False

    def get_flag(self, flag):
        return self.__fmem[flag]

    def flags(self):
        return self.__fmem


# an object where instructions are stored accordingly
class InstructionMemory:
    def __init__(self):
        self.__memory = {}

    def i_at(self, address):
        return self.__memory[address]

    def i_set(self, address, instruction):
        self.__memory[address] = instruction

    def i_line(self, address):
        return self.__memory[address]

    def __str__(self):
        result = ""
        for (address, instructions) in self.__memory.items():
            instruction_data = ""
            for instruction in instructions:
                instruction_data += " " + str(instruction)
            result += "0x" + str(address) + " | " + instruction_data + "\n"
        return result


# arithmetic and logic operations used by PVM
class ALOperation:
    @staticmethod
    def add(op1, op2):
        return op1 + op2

    @staticmethod
    def sub(op1, op2):
        return op1 - op2

    @staticmethod
    def mul(op1, op2):
        return op1 * op2

    @staticmethod
    def idiv(op1, op2):
        return int(op1 / op2)

    @staticmethod
    def div(op1, op2):
        return op1 / op2

    @staticmethod
    def ie(op1, op2):
        return op1 == op2

    @staticmethod
    def ine(op1, op2):
        return not op1 == op2

    @staticmethod
    def ig(op1, op2):
        return op1 > op2

    @staticmethod
    def il(op1, op2):
        return op1 < op2

    @staticmethod
    def ige(op1, op2):
        return op1 >= op2

    @staticmethod
    def ile(op1, op2):
        return op1 <= op2


# PVM
# Plas Virtual Machine
# a place where instructions are executed
class PVM:
    def __init__(self, raw_instruction):
        self.__raw_instruction = raw_instruction
        self.__amem = AbstractMemory()  # abstract memory
        self.__fmem = FlagMemory()  # flag memory
        self.__insmem = InstructionMemory()  # instruction memory
        self.__pvm_operations = (
            self.__ins_putc,
            self.__ins_load,
            self.__ins_go,
            self.__ins_exit,
            self.__ins_eval,
            self.__ins_ifeq,
            self.__ins_ifne,
            self.__ins_ifgt,
            self.__ins_iflt,
            self.__ins_ifge,
            self.__ins_ifle,
            self.__ins_add,
            self.__ins_sub,
            self.__ins_mul,
            self.__ins_idiv,
            self.__ins_div,
            self.__ins_home,
            self.__ins_log
        )

        self.__init_instruction_memory()
        self.total_ins = len(self.__raw_instruction.keys())
        self.instruction_pointer = 0x00000000
        self.temporary_address = 0x00000000
        self.__start_execution(self.instruction_pointer)
        sys.exit(SysExit.EXIT_SUCCESS)

    def __start_execution(self, current_address):
        if current_address > self.total_ins - 1:
            return
        self.__execute__address(current_address)
        self.__start_execution(self.instruction_pointer)

    def __execute__address(self, address):
        instruction = self.__insmem.i_at(address)[0]
        args = self.__insmem.i_at(address)[1:]
        self.__pvm_operations[instruction - 1](args)

    def __ins_putc(self, args):
        op1 = chr(int(self.__amem.getmem(args[0].get_data())))
        sys.stdout.write("%c" % op1)
        self.__next_instruction()

    def __ins_load(self, args):
        op1, op2 = args[0:2]
        op2_val = PVM.__extract_value(op2, self.__amem)
        self.__amem.setmem(op1.get_data(), op2_val)
        self.__next_instruction()

    def __ins_go(self, args):
        op1 = args[0].get_data()
        self.__store_instruction()
        self.__change_instruction_address(op1)
        self.__execute__address(op1)

    def __ins_exit(self, args):
        op1 = PVM.__extract_value(args[0], self.__amem)
        sys.exit(int(op1))

    def __ins_eval(self, args):
        op1 = PVM.__extract_value(args[0], self.__amem)
        op2 = PVM.__extract_value(args[1], self.__amem)
        self.__adjust_flags_evalop(op1, op2)
        self.__next_instruction()

    def __ins_ifeq(self, args):
        op1 = args[0].get_data()
        if self.__fmem.get_flag(FMT.flags[FMT.FEQ]):
            self.__change_instruction_address(op1)
            self.__execute__address(op1)
            return
        self.__next_instruction()
        # self.__start_execution(self.instruction_pointer + 1)

    def __ins_ifne(self, args):
        op1 = args[0].get_data()
        if self.__fmem.get_flag(FMT.flags[FMT.FNE]):
            self.__change_instruction_address(op1)
            self.__execute__address(op1)
            return
        self.__next_instruction()
        # self.__start_execution(self.instruction_pointer + 1)

    def __ins_ifgt(self, args):
        op1 = args[0].get_data()
        if self.__fmem.get_flag(FMT.flags[FMT.FGT]):
            self.__change_instruction_address(op1)
            self.__execute__address(op1)
            return
        self.__next_instruction()
        # self.__start_execution(self.instruction_pointer + 1)

    def __ins_iflt(self, args):
        op1 = args[0].get_data()
        if self.__fmem.get_flag(FMT.flags[FMT.FLT]):
            self.__change_instruction_address(op1)
            self.__execute__address(op1)
            return
        self.__next_instruction()
        # self.__start_execution(self.instruction_pointer + 1)

    def __ins_ifge(self, args):
        op1 = args[0].get_data()
        if self.__fmem.get_flag(FMT.flags[FMT.FGE]):
            self.__change_instruction_address(op1)
            self.__execute__address(op1)
            return
        self.__next_instruction()
        # self.__start_execution(self.instruction_pointer + 1)

    def __ins_ifle(self, args):
        op1 = args[0].get_data()
        if self.__fmem.get_flag(FMT.flags[FMT.FLE]):
            self.__change_instruction_address(op1)
            self.__execute__address(op1)
            return
        self.__next_instruction()
        # self.__start_execution(self.instruction_pointer + 1)

    def __ins_add(self, args):
        op1, op2 = args[0:2]
        op2_val = PVM.__extract_value(op2, self.__amem)
        res = ALOperation.add(self.__amem.getmem(op1.get_data()), op2_val)
        self.__amem.setmem(op1.get_data(), res)
        self.__next_instruction()

    def __ins_sub(self, args):
        op1, op2 = args[0:2]
        op2_val = PVM.__extract_value(op2, self.__amem)
        res = ALOperation.sub(self.__amem.getmem(op1.get_data()), op2_val)
        self.__amem.setmem(op1.get_data(), res)
        self.__next_instruction()

    def __ins_mul(self, args):
        op1, op2 = args[0:2]
        op2_val = PVM.__extract_value(op2, self.__amem)
        res = ALOperation.mul(self.__amem.getmem(op1.get_data()), op2_val)
        self.__amem.setmem(op1.get_data(), res)
        self.__next_instruction()

    def __ins_idiv(self, args):
        op1, op2 = args[0:2]
        op2_val = PVM.__extract_value(op2, self.__amem)
        if op2_val == 0:
            Log.e("runtime error", "zero division error")
            Log.e("reason", "division by zero at line " + str(list(self.__raw_instruction.values()[1])))
            sys.exit(SysExit.EXIT_ZERO_DIVISION_ERROR)

        res = ALOperation.idiv(self.__amem.getmem(op1.get_data()), op2_val)
        self.__amem.setmem(op1.get_data(), res)
        self.__next_instruction()

    def __ins_div(self, args):
        op1, op2 = args[0:2]
        op2_val = PVM.__extract_value(op2, self.__amem)
        if op2_val == 0:
            Log.e("runtime error", "zero division error")
            Log.e("reason", "division by zero at line " + \
                  str(list(self.__raw_instruction.values())[self.instruction_pointer][1]))

            sys.exit(SysExit.EXIT_ZERO_DIVISION_ERROR)

        res = ALOperation.div(self.__amem.getmem(op1.get_data()), op2_val)
        self.__amem.setmem(op1.get_data(), res)
        self.__next_instruction()

    def __ins_home(self, args=None):
        self.__change_instruction_address(self.temporary_address + 0x01)
        self.__start_execution(self.instruction_pointer)

    def __ins_log(self, args):
        op1 = args[0]
        sys.stdout.write("%s\n" % self.__amem.getmem(op1.get_data()))
        self.__next_instruction()

    def __init_instruction_memory(self):
        for (address, ins_wlan) in self.__raw_instruction.items():
            ins_arg = []
            for expression in ins_wlan[0]:
                if expression.get_type() == TokenType.TKN_INS:
                    ins_arg.append(InstructionTable.INS[expression.get_data()])
                    continue
                ins_arg.append(expression)
            self.__insmem.i_set(address, ins_arg)

    # after eval operation flag registers are adjust here
    def __adjust_flags_evalop(self, op1, op2):
        if op1 == op2:
            self.__fmem.enable_flag(FMT.flags[FMT.FEQ])
            self.__fmem.enable_flag(FMT.flags[FMT.FNE])
            self.__fmem.disable_flag(FMT.flags[FMT.FGT])
            self.__fmem.disable_flag(FMT.flags[FMT.FLT])
            self.__fmem.enable_flag(FMT.flags[FMT.FGE])
            self.__fmem.enable_flag(FMT.flags[FMT.FLE])
        else:
            self.__fmem.disable_flag(FMT.flags[FMT.FEQ])
            self.__fmem.enable_flag(FMT.flags[FMT.FNE])
            if op1 > op2:
                self.__fmem.enable_flag(FMT.flags[FMT.FGT])
                self.__fmem.disable_flag(FMT.flags[FMT.FLT])
                if op1 >= op2:
                    self.__fmem.disable_flag(FMT.flags[FMT.FLE])
                    self.__fmem.disable_flag(FMT.flags[FMT.FGE])
            else:
                self.__fmem.disable_flag(FMT.flags[FMT.FGT])
                self.__fmem.enable_flag(FMT.flags[FMT.FLT])
                if op1 <= op2:
                    self.__fmem.enable_flag(FMT.flags[FMT.FLE])
                    self.__fmem.disable_flag(FMT.flags[FMT.FGE])

    def __next_instruction(self):
        self.instruction_pointer += 1

    def __change_instruction_address(self, address):
        self.instruction_pointer = address

    def __store_instruction(self):
        self.temporary_address = self.instruction_pointer

    @staticmethod
    def __is_float(num):
        if re.fullmatch(r'-?([0-9]*)\.[0-9]*', num):
            return True
        return False

    @staticmethod
    def __extract_value(op, mem):
        if op.get_type() == TokenType.TKN_VAL:
            if PVM.__is_float(op.get_data()):
                return float(op.get_data())
            else:
                return int(op.get_data())

        if op.get_type() == TokenType.TKN_MEM:
            address_value = mem.getmem(op.get_data())
            if PVM.__is_float(str(address_value)):
                return float(address_value)
            else:
                return int(address_value)


class MemoryAddressTable:
    memory_addresses = {
        "$0": 0x000,
        "$1": 0X001,
        "$2": 0x002,
        "$3": 0X003,
        "$4": 0X004,
        "$5": 0X005,
        "$6": 0X006,
        "$7": 0x007,
        "$8": 0x008,
        "$9": 0x009,
        "$a": 0x00a,
        "$b": 0x00b,
        "$c": 0x00c,
        "$d": 0x00d,
        "$e": 0x00e,
        "$f": 0x00f
    }


class AbstractMemory:
    def __init__(self):
        self.__memory = {}
        self.__memory_table = MemoryAddressTable.memory_addresses
        for address in self.__memory_table.keys():
            self.__memory[address] = 0

    def setmem(self, address, value):
        self.__memory[address] = value

    def getmem(self, address):
        return self.__memory[address]


# system exit types
class SysExit:
    EXIT_SUCCESS = 0
    EXIT_SYNTAX_ERROR = 9
    EXIT_ZERO_DIVISION_ERROR = 10


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


class PLAS_SYNTAX:
    SYNTAX_S = "putc     2        \n" + \
               "load     2     2|3\n" + \
               "go       6        \n" + \
               "exit     2|3      \n" + \
               "eval     2|3   2|3\n" + \
               "ifeq     6        \n" + \
               "ifne     6        \n" + \
               "ifgt     6        \n" + \
               "iflt     6        \n" + \
               "ifge     6        \n" + \
               "ifle     6        \n" + \
               "add      2     2|3\n" + \
               "sub      2     2|3\n" + \
               "mul      2     2|3\n" + \
               "idiv     2     2|3\n" + \
               "div      2     2|3\n" + \
               "home              \n" + \
               "log      2        \n"


class SyntaxBuilder:
    __INSTRUCTION_INDEX = 0
    __REQUIREMENT_INDEX = 1

    def __init__(self, rules):
        self.syntax_rules = rules
        self.__preprocessor = Preprocessor(self.syntax_rules)
        self.__preprocessed = self.__preprocessor.get_preprocessed()
        self.__pre_rules = []
        for syntax_tokens in self.__preprocessed:
            self.__pre_rules.append(syntax_tokens[0])

        # initialize syntax table
        self.__rule_table = []
        for rule in self.__pre_rules:
            self.__rule_table.append(rule.split(" "))

        self.rule_tree = {}
        self.__add_rules()

    def __add_rules(self):
        for item in self.__rule_table:
            instruction = item[SyntaxBuilder.__INSTRUCTION_INDEX]
            requirements = item[SyntaxBuilder.__REQUIREMENT_INDEX:]
            requirement_list = []
            for requirement in requirements:
                req = requirement.split("|")
                options = []
                for r in req:
                    options.append(int(r))
                requirement_list.append(options)
            self.rule_tree[instruction] = requirement_list

    def __str__(self):
        string = ""
        for (instruction, requirement) in self.rule_tree.items():
            string += "[{0} [{1}]]\n".format(instruction, requirement)
        return string

    def get_rules(self):
        return self.rule_tree


class SyntaxMatcher:
    def __init__(self, syntax_rule, syntax):
        self.syntax_rule = syntax_rule
        self.syntax = syntax
        self.checked = 0

    def matches(self):
        for rule in self.syntax_rule:
            matched = False
            for option in rule:
                if self.syntax[self.checked].get_type() == option:
                    matched = True
            if not matched:
                return False

            self.checked += 1

        return True

    def get_checked(self):
        return self.checked


class LabelTable:
    def __init__(self):
        self.table = {}

    def add(self, label: str, line: int):
        if label in self.table:
            return False

        self.table[label] = line
        return True

    def get_table(self) -> dict:
        return self.table


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.labelTable = LabelTable()
        self.rule_builder = SyntaxBuilder(PLAS_SYNTAX.SYNTAX_S)
        self.rules = self.rule_builder.get_rules()
        self.__address_table = {}
        self.__evaluate_labels()
        self.__check_starting_syntax()
        self.__replace_labels()
        self.__match_syntax()
        self.__build_addresses()
        self.__organize_address()
        # self.__log__labels()

    def get_raw_instructions(self):
        return self.tokens

    # check for instructions at start
    def __check_starting_syntax(self):
        for (line, line_token) in self.tokens.items():
            if not line_token[0].get_type() == TokenType.TKN_INS:
                Log.e("error", "instruction is expected at line " + str(line))
                Log.e("reason", "given is " + " [ " + line_token[0].get_data() + " ] not instruction")
                sys.exit(SysExit.EXIT_SYNTAX_ERROR)

    def __match_syntax(self):
        for (line, lineToken) in self.tokens.items():
            instruction = lineToken[0].get_data()
            expressions = lineToken[1:]
            rule = self.rules[instruction]
            syntax_matcher = SyntaxMatcher(rule, expressions)
            if not len(lineToken[1:]) == len(rule):
                Log.e("error", "expected argument not found at line " + str(line))
                sys.exit(SysExit.EXIT_SYNTAX_ERROR)

            if not syntax_matcher.matches():
                expected = "( "
                for e in rule[syntax_matcher.get_checked() - 1]:
                    expected += TTC.get_type(e) + " "
                expected += " )"
                found = expressions[syntax_matcher.get_checked()].get_data()
                message = "expected {0} but found ( {1} ) at line {2}".format(expected, found, line)
                Log.e("error", message)
                sys.exit(SysExit.EXIT_SYNTAX_ERROR)

    def __evaluate_labels(self):
        for (line, line_token) in self.tokens.items():
            if Parser.__has_directive(line_token):
                li = 0  # label index
                for token in line_token:
                    if token.get_type() == TokenType.TKN_SYM \
                            and token.get_data() == ':':
                        if li + 1 >= len(line_token):
                            Log.e("error", "unable to locate label at line " + str(line))
                            sys.exit(SysExit.EXIT_SYNTAX_ERROR)

                        if not line_token[li + 1].get_type() == TokenType.TKN_LBL:
                            Log.e("error", "invalid label provided at line " + str(line))
                            sys.exit(SysExit.EXIT_SYNTAX_ERROR)

                        if len(line_token) > li + 2:
                            Log.e("error", "definition not allowed after label")
                            Log.e("unacceptable definition", "error at line " + str(line))
                            sys.exit(SysExit.EXIT_SYNTAX_ERROR)

                        if not self.labelTable.add(line_token[li + 1].get_data(), line):
                            Log.e("error", "label cannot be redefined")
                            Log.e("error", "label redefined at line " + str(line))
                            sys.exit(SysExit.EXIT_SYNTAX_ERROR)

                        line_token = line_token[:li]
                        self.tokens[line] = line_token

                    li += 1

    def __replace_labels(self):
        for (line, line_token) in self.tokens.items():
            if Parser.__has_directive(line_token):
                li = 0
                for token in line_token:
                    if token.get_type() == TokenType.TKN_SYM \
                            and token.get_data() == '@':
                        if li + 1 >= len(line_token):
                            Log.e("error", "unable to locate label at line " + str(line))
                            sys.exit(SysExit.EXIT_SYNTAX_ERROR)

                        if not line_token[li + 1].get_type() == TokenType.TKN_LBL:
                            Log.e("error", "invalid label provided at line " + str(line))
                            sys.exit(SysExit.EXIT_SYNTAX_ERROR)

                        if len(line_token) > li + 2:
                            Log.e("error", "syntax not allowed after label")
                            sys.exit(SysExit.EXIT_SYNTAX_ERROR)

                        # check for label in label table
                        label = line_token[li + 1].get_data()
                        if not label in self.labelTable.get_table():
                            Log.w("error label [ " + label + " ] could not be found")
                            Log.e("error", "label not found at line " + str(line))
                            sys.exit(SysExit.EXIT_SYNTAX_ERROR)

                        line_token = line_token[:li + 1]
                        token = Token.create_from(TokenType.TKN_ADR, self.labelTable.get_table()[label])
                        line_token[li] = token
                        self.tokens[line] = line_token
                    li += 1

    def __build_addresses(self):
        start_ins = 0
        for (line, instruction) in self.tokens.items():
            self.__address_table[line] = start_ins
            start_ins += 1

    def __organize_address(self):
        new_tokens = {}
        for (line, each_instructions) in self.tokens.items():
            new_tokens[self.__address_table[line]] = (each_instructions, line)

        # address and instruction with origin line : ins_wline
        for (address, ins_wline) in new_tokens.items():
            for instruction in ins_wline[0]:
                if instruction.get_type() == TokenType.TKN_ADR:
                    instruction.set_data(self.__address_table[instruction.get_data()])

        self.tokens = new_tokens

    @staticmethod
    def __has_directive(line):
        for token in line:
            if token.get_type() == TokenType.TKN_SYM:
                if token.get_data() == '@' or token.get_data() == ':':
                    return True

        return False

    def __log__labels(self):
        for token in self.tokens:
            for tkn in self.tokens[token]:
                print("{0} ".format(tkn), end="")
            print()

    def to_file(self, file):
        data = ""
        if len(self.tokens.keys()) == 0:
            return
        large_line = len(str(max(self.tokens.keys())))
        for (line, line_tokens) in self.tokens.items():
            line_data = ""
            token_data = ""
            for token in line_tokens[0]:
                line_data += str(token.get_data()) + " "
                token_data += str(token) + " "
            _line = "0x%{0}d: %-20s | %5s\n".format(large_line)
            _line = _line % (line, line_data, token_data)
            # line = "%5d: %-20s | %5s\n" % (line, line_data, token_data)
            data += _line

        with open(file, "w+") as f:
            f.write(data)


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


class ASCIIHelper:
    ALPHA_REGEX = r"[a-zA-Z]"
    ALPHANUM_REGEX = r"[a-zA-Z0-9]"
    NUM_REGEX = r"[0-9]+"
    SYM_REGEX = r"[\!\@\#\$\%\^\&\*\(\)\-\_\=\+\[\{\]\}\;\:\'\\\"\,\<\.\>\/\?\`\~\| \t]"

    @staticmethod
    def is_alpha(c: chr) -> bool:
        if re.fullmatch(ASCIIHelper.ALPHA_REGEX, c):
            return True

        return False

    @staticmethod
    def is_alphanum(c: chr) -> bool:
        if re.fullmatch(ASCIIHelper.ALPHANUM_REGEX, c):
            return True

        return False

    @staticmethod
    def is_num(c: chr) -> bool:
        if re.fullmatch(ASCIIHelper.NUM_REGEX, c):
            return True

        return False

    @staticmethod
    def is_special_char(c: chr) -> bool:
        if re.fullmatch(ASCIIHelper.SYM_REGEX, c):
            return True

        return False


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


class Preprocessor:
    def __init__(self, source: str):
        self.source = source
        self.preprocessed = []
        self.__preprocess()

    def __preprocess(self):
        line = 1
        for stream in self.source.split('\n'):
            clean_stream = ""
            stream = stream.strip().replace('\t', ' ')
            if stream.startswith("#"):
                line += 1
                continue

            if stream == "" or stream is None:
                line += 1
                continue

            # clean space and comment after a code
            space_seen = False
            for c in stream:
                if c == '#':
                    break
                if not c == chr(0x20) or not space_seen:
                    clean_stream += c
                    space_seen = False
                if c == chr(0x20):
                    space_seen = True

            self.preprocessed.append([clean_stream.strip(), line])
            line += 1

    def get_preprocessed(self) -> list:
        return self.preprocessed


class SourceStream:
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
        return self.stream

    def __str__(self) -> str:
        return self.stream


class Log:
    __GREEN = '\033[1;32m'
    __NORM = '\033[0;00m'
    __RED = '\033[1;31m'

    @staticmethod
    def d(key: str, message: str):
        sys.stdout.write(
            Log.__GREEN + str(key) +
            str(": ") +
            Log.__NORM +
            str(message) +
            chr(0x0a)
        )

    @staticmethod
    def e(key: str, message: str):
        sys.stdout.write(
            Log.__RED + str(key) + str(": ") +
            Log.__NORM +
            str(message) +
            chr(0x0a)
        )

    @staticmethod
    def w(message: str):
        sys.stdout.write(Log.__NORM + str(message) + chr(0x0a))


class Plas:
    def __init__(self, file):
        ss = SourceStream(file)
        if ss.get_stream() == "":
            return

        preprocessor = Preprocessor(ss.get_stream())
        tokenizer = Tokenizer(preprocessor.get_preprocessed())
        tokenizer.to_file(file+".tkn")
        parser = Parser(tokenizer.get_tokens())
        PVM(raw_instruction=parser.get_raw_instructions())


class CompileConfiguration:
    TOKEN_OUT = False
    PARSE_OUT = False


def main():
    if len(sys.argv) <= 1:
        Log.e("error", "unable to start process without a file")
        Log.w("source file is needed")
        sys.exit(1)

    source_file = sys.argv[1]
    if not os.path.exists(source_file):
        Log.w("file not found %s" % source_file)
        sys.exit(2)

    Plas(source_file)


if __name__ == "__main__":
    main()
