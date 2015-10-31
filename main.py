import argparse
import os
import subprocess
import re
import yaml

import pdb

command = "clang-tidy {0} --"

type_to_clang_check = { 
        'IfAssign' : 'clang-diagnostic-parentheses', 
        'SwitchBool' : 'clang-diagnostic-switch-bool'
        }

class Error:
    def __init__(self, type, cost):
        self.type = type
        self.cost = cost
        self.message = '[' + type_to_clang_check[self.type] + ']'

def parse_config(config):
    """Parses the marking scheme file.

    :param config: Configuration file containing the mistakes the grader will be looking for and the penalties associated with them.
                   Note that this file is in the YAML format.
    """
    errors = []
    conf = open(config)
    data = yaml.safe_load(conf)
    conf.close()
    for d in data:
        errors.append(Error(d['error']['type'], d['error']['cost']))

    return errors

def init_parser():
    """Initializes the CorrectUS arguement parser.
    """
    parser = argparse.ArgumentParser(description="CorrectUS options:")
    parser.add_argument('-dir=', dest='dir', metavar='directory', 
                        help="""Specifies the top level directory containing the assignments to grade. 
                                When the value is empty it will assume the current directory is the one containing the assignment""")
    #TODO: Add argument for outputting to file or stdout
    parser.add_argument('-config=', dest='config', metavar='config file', 
                        help="Specifies the configuration file in YAML format. When the value is empty it will use the default configuration file provided.")

    return parser

def grade(student_dir, marking_scheme):
    """Grades a student homework based on a marking scheme. 
    This will generate a report to inform the student of the mistakes he made and the penalty associated with each mistake.

    :param student_dir: Directory containint the student homework
    :param marking_scheme: Mistakes and the penalties associated with them that the grader will be looking for.
    """
    total_penalty = 0
    for f in os.listdir(directory):
        extension = os.path.splitext(f)[1][1:]
        if extension in ["cpp", "h"]:
            p = subprocess.Popen(command.format(directory + f).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = p.communicate()[0]
            osplit = output.split('\n')
            for line in osplit:
                if "warning:" in line:
                    infos = line.split(':')
                    found_error = next((x for x in marking_scheme if x.message in line), None)
                    if found_error is not None:
                        print "Mistake:{0}".format(re.sub("\[[a-zA-Z\.\-]+\]",'', infos[4]))
                        print "File: {0}, Line {1}, Column {2}".format(os.path.basename(infos[0]), infos[1], infos[2])
                        print "Penalty: {0}".format(found_error.cost)
                        print ""
                        total_penalty += found_error.cost


def main():
    parser = init_parser()
    args = parser.parse_args()
    directory = args.dir

    marking_scheme = parse_config(args.config)

    if os.path.isdir(directory):
        for student_dir in directory:
            if os.path.isdir(student_dir):
                grade(student_dir, marking_scheme)
    else:
        print "Not a valid directory path"

if __name__ == '__main__':
    main()

