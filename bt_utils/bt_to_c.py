from bt_utils.c_templates import make_source
from ._tokens import *
from .grammar import BT_Grammar
from .c_templates import *
import os

class BT_to_C(BT_Grammar):
    def __init__(self, bt_file_name):
        super().__init__(bt_file_name)
        make_header(self.h_file_name, [])
        make_source(self.c_file_name, list(self._vars_dict["FUNCS"].keys()), self._convert_to_c_str(), 0)
        

    def compile(self, compiler_path):
        # files = os.listdir()
        # if (self.c_file_name not in files):
        #     self.__make_c_file()
            
        os.system(f"{compiler_path} {self.c_file_name} -o {self.bin_name}")

    def run(self):
        os.system(f"./{self.bin_name}")