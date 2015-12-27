import os
import subprocess
import yaml

class GradingEngine:
    def __init__(self):
        self.command = "clang-tidy {0} -- -Weverything"

    def set_marking_scheme(self, marking_scheme):
        self.marking_scheme = marking_scheme

    def grade_all(self, directory):
        if os.path.isdir(directory):
            for student_dir in os.listdir(directory):
                complete_student_dir = directory + student_dir + '/'
                if os.path.isdir(complete_student_dir):
                    self.grade_student(complete_student_dir)

    def grade_student(self, student_dir):
        total_penalty = 0
        for _, _, fnames in os.walk(student_dir):
            for fname in fnames:
                extension = os.path.splitext(fname)[1][1:]
                if extension in ["cpp", "h"]:
                    p = subprocess.Popen(self.command.format(student_dir + fname).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output = p.communicate()[0]
                    osplit = output.split('\n')
                    for line in osplit:
                        if "warning:" in line:
                            infos = line.split(':')
                            clang_msg = infos[4]
                            clang_msg = clang_msg[clang_msg.rfind('['):]
                            # By default, there's a 2 point penalty for a warning
                            penalty = self.marking_scheme[clang_msg] if clang_msg in self.marking_scheme else 2

                            print "Mistake:{0}".format(infos[4].replace(clang_msg, ''))
                            print "File: {0}, Line {1}, Column {2}".format(os.path.basename(infos[0]), infos[1], infos[2])
                            print "Penalty: {0}\n".format(penalty)
                            total_penalty += penalty
        print "Total penalty: {0}\n".format(total_penalty)
