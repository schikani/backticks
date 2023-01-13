from ._tokens import *
from .grammar import BT_Grammar
from .c_templates import *
from .utils import hashing
from os.path import exists, basename
import os


class BT_to_C(BT_Grammar):
    if "pcf" not in os.listdir("."):
        os.mkdir("pcf")

    if "hash" not in os.listdir("./pcf/"):
        os.mkdir("./pcf/hash")

    if "bin" not in os.listdir("."):
        os.mkdir("bin")

    def __init__(self, bt_file_path, main_file=True):
        super().__init__(bt_file_path)

        if main_file:
            make_bt_builtins_header()
            make_builtins_source()

        make_source(self.c_file_name, self._private_func_list, self._funcs_impl, self._convert_to_c_str(self.tokens, self._vars_dict["GLOBALS"]["global_vars"]), 0, main_file)
        make_header(self.h_file_name, self._public_func_list, self._global_vars_list, self._class_structs, main_file, self._includes)
    
        self.hash_file_path = f"./pcf/hash/{self.bin_name}"

    def check_and_compile(self, dpcf):

        # List of C source files
        sources = list()

        # List of Boolean values for file/s to compile
        good_to_go = []

        # Append C current file and imported files in conf
        with open("./pcf/conf", "a") as file:

            for i in self._imports_dict.values():
                file.write(i +".c" + SPACE + NEWLINE)

            file.write(self.bin_name +".c" + SPACE)

        with open("./pcf/conf", "r") as file:
            for src in file:
                sources.append(src.strip())

        # Remove temp conf file containing C file names
        os.remove("./pcf/conf")


        # Append BT current file and imported files in conf
        with open("./pcf/bt_paths", "a") as bt_path_file:

            bt_path_file.write(self.bt_file_path + NEWLINE)
            try:
                base_path = self.bt_file_path[:self.bt_file_path.rindex("/")+1]

            # if the path doesn't have folder included
            except ValueError:
                base_path = self.bt_file_path

            for i in self._imports_dict.values():
                bt_path_file.write(base_path + i +".bt" + NEWLINE)

        
        print("-" * 50)
        print("Files for compilation:\n")

        with open("./pcf/bt_paths", "r") as bt_paths:
            for path in bt_paths:

                bt_source = path.strip()
                hash_s = f"./pcf/hash/{basename(bt_source)[:basename(bt_source).index('.bt')]}"
                new_hash = hashing.sha1_hashing(bt_source)

                if exists(hash_s):
                    with open(hash_s, "r") as current_hash:
                        current_hash = current_hash.read()
                else:
                    current_hash = ""

                if current_hash.strip() != new_hash:
                    good_to_go.append(True)
                    print(f"Adding: {basename(bt_source)}")
                    with open(hash_s, "w") as hf:
                        hf.write(new_hash)
                else:
                    good_to_go.append(False)
                    print(f"Ignoring: {basename(bt_source)}")

        print("-" * 50)

        # Remove temp bt_paths file containing bt file paths
        os.remove("./pcf/bt_paths")
        
        if good_to_go.count(True):
            self.compile(sources, "gcc")

        # Delete Pre-compiling folder
        if dpcf:
            os.system("rm -rf ./pcf")
        
    
    def compile(self, sources, compiler_path):
        
        # Add builtins
        c_sources = "./pcf/_bt_builtins_.c "
        for s in sources:
            c_sources += "./pcf/" + s + SPACE

        os.system(f"{compiler_path} {c_sources} -o ./bin/{self.bin_name} -lm")        


    def run(self):
        os.system(f"./bin/{self.bin_name}")