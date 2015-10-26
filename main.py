import argparse
import os
from subprocess import call

import pdb

def main():
    parser = argparse.ArgumentParser(description="CorrectUS arguments parser")
    parser.add_argument('dir', help="Top level directory containing the assignments to grade", action='store')

    args = parser.parse_args()
    directory = args.dir

    if os.path.isdir(directory):
        for f in os.listdir(directory):
            extension = os.path.splitext(f)[1][1:]
            if extension in ["cpp", "h"]:
                call(["clang-tidy", directory + f, "--"])
    else:
        print "Not a valid directory path"

if __name__ == '__main__':
    main()

