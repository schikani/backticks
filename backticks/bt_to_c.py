from ._tokens import *
from .grammar import BT_Grammar
from .c_templates import *
import os


class BT_to_C(BT_Grammar):
    if "C" not in os.listdir("."):
        os.mkdir("C")

    if "bin" not in os.listdir("."):
        os.mkdir("bin")

    def __init__(self, bt_file_path, main_file=True):
        super().__init__(bt_file_path)
        # print(self._func_list)

        if main_file:
            make_bt_builtins_header()
            make_builtins_source()

        make_source(self.c_file_name, self._private_func_list, self._funcs_impl, self._convert_to_c_str(self.tokens, self._vars_dict["GLOBALS"]["global_vars"]), 0, main_file)
        make_header(self.h_file_name, self._public_func_list, self._global_vars_list, main_file, self._includes)
        
    
    def compile(self, compiler_path, del_c_h_files=False):
        # print("Compiling..")

        src_files = set()

        # Append current file in conf
        with open("./C/conf", "a") as file:
            file.write(self.bin_name +".c" + SPACE)

        with open("./C/conf", "r") as file:
            for src in file:
                src_files.add(src.strip())
        
        # print(src_files)
        
        # Add builtins
        c_sources = "./C/_bt_builtins_.c "
        for s in list(src_files):
            c_sources += "./C/" + s + SPACE

        os.system(f"{compiler_path} {c_sources} -o ./bin/{self.bin_name} -lm")

        os.remove("./C/conf")

        if del_c_h_files:
            os.system("rm -rf ./C")

        # print("Finished.")
        


    def run(self):
        os.system(f"./bin/{self.bin_name}")