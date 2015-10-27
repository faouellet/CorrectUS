import argparse
import os
import subprocess
import re

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
                p = subprocess.Popen(["clang-tidy", directory + f, "--"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = p.communicate()[0]
                osplit = output.split('\n')
                for line in osplit:
                    if "warning:" in line:
                        infos = line.split(':')
                        print "Mistake:{0}".format(re.sub("\[[a-zA-Z\.\-]+\]",'', infos[4]))
                        print "File: {0}, Line {1}, Column {2}".format(os.path.basename(infos[0]), infos[1], infos[2])
                        print ""
    else:
        print "Not a valid directory path"

if __name__ == '__main__':
    main()

