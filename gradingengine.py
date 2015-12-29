import os
import subprocess

class GradingEngine:
    def __init__(self):
        self.command = "clang-tidy {0} -- -Weverything"
        self.marking_scheme = {}

    def set_marking_scheme(self, marking_scheme):
        for err in marking_scheme.values():
            if err.is_enabled:
                self.marking_scheme[err.check] = err.penalty
        print (self.marking_scheme)

    def grade_all(self, hw_root_dir, res_dir):
        if os.path.isdir(hw_root_dir):
            for student_dir in os.listdir(hw_root_dir):
                complete_student_dir = os.path.join(hw_root_dir, student_dir)
                if os.path.isdir(complete_student_dir):
                    student_result = self.grade_student(complete_student_dir)
                    with open('%s/%s.txt' % (res_dir, student_dir), 'w+') as student_res_file:
                        student_res_file.write(student_result)

    def grade_student(self, student_dir):
        total_penalty = 0
        grading_msg = []
        for _, _, fnames in os.walk(student_dir):
            for fname in fnames:
                extension = os.path.splitext(fname)[1][1:]
                if extension in ["cpp", "h"]:
                    p = subprocess.Popen(self.command.format(os.path.join(student_dir, fname)).split(' '), 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output = p.communicate()[0]
                    osplit = output.decode('utf-8').split('\n')
                    for line in osplit:
                        if "warning:" in line:
                            infos = line.split(':')
                            clang_msg = infos[4]
                            clang_msg = clang_msg[clang_msg.rfind('['):]
                            marking_key = clang_msg.replace('[','')
                            marking_key = marking_key.replace(']','')
                            if marking_key in self.marking_scheme: 
                                grading_msg.append("Mistake:{0}".format(infos[4].replace(clang_msg, '')))
                                grading_msg.append("File: {0}, Line: {1}, Column: {2}".format(os.path.basename(infos[0]), infos[1], infos[2]))
                                grading_msg.append("Penalty: %i\n" % self.marking_scheme[marking_key])
                                total_penalty += self.marking_scheme[marking_key]
        grading_msg.append("Total penalty: %i\n" % total_penalty)
        return '\n'.join(grading_msg)
