from ._tokens import *
from .grammar import BT_Grammar
from .c_templates import make_source, make_header
import os


class BT_to_C(BT_Grammar):
    if "C" not in os.listdir("."):
        os.mkdir("C")

    if "bin" not in os.listdir("."):
        os.mkdir("bin")

    def __init__(self, bt_file_name):
        super().__init__(bt_file_name)
        # print(self._func_list)
        make_source(self.c_file_name, self._private_func_list, self._funcs_impl, self._convert_to_c_str(self.tokens, self._vars_dict["GLOBALS"]["global_vars"]), 0)
        make_header(self.h_file_name, self._public_func_list, self._global_vars_list)
        

    def compile(self, compiler_path):
        os.system(f"{compiler_path} ./C/{self.c_file_name} -o ./bin/{self.bin_name} -lm")



    def run(self):
        os.system(f"./bin/{self.bin_name}")