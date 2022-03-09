#!/usr/bin/python3

# from bt_utils import BT_to_C

import sys

# Include backticks module
sys.path.insert(1, '../')
from bt_utils import BT_to_C


argc = len(sys.argv)
argv = sys.argv[1:]

src = BT_to_C(argv[0])
print(src.tokens)


src.compile("gcc")
src.run()

