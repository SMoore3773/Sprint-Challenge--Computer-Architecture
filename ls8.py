import sys
from cpu import *

if len(sys.argv) != 2:
    print("must have 2 args passed in command line")

else:

    cpu = CPU()

    cpu.load(sys.argv[1])
    cpu.run()
