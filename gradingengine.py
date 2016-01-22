import argparse
import os
import re
import subprocess


class GradingEngine:
    def __init__(self):
        command = "clang-tidy"
        extra_args = ["--","-Weverything"]
        self.marking_scheme = {}
        clang_msg_re = re.compile("(?P<filepath>.*):(?P<line>[0-9]+):(?P<column>[0-9]+): warning: (?P<msg>.*)\[(?P<check>.*)\]")


    def set_marking_scheme(self, marking_scheme):
        for err in marking_scheme.values():
            if err.is_enabled:
                self.marking_scheme[err.check] = err.penalty


    def grade_all(self, hw_root_dir, res_dir, correct_exe, data_dir):
        if os.path.isdir(hw_root_dir):
            for student_dir in os.listdir(hw_root_dir):
                complete_student_dir = os.path.join(hw_root_dir, student_dir)
                if os.path.isdir(complete_student_dir):
                    student_result = self.grade_student(complete_student_dir, correct_exe, data_dir)
                    with open('%s/%s.txt' % (res_dir, student_dir), 'w+') as student_res_file:
                        student_res_file.write(student_result)


    def grade_student(self, student_dir, correct_exe, data_dir):
        student_res = self.grade_correctness(student_dir, correct_exe, data_dir)
        student_res = student_res + self.grade_includes(student_dir)
        student_res = student_res + self.grade_coding_standards(student_dir)
        student_res = student_res + self.grade_error_and_doc(student_dir)


    def grade_correctness(self, student_dir, correct_exe, data_dir):
        pass


    def grade_coding_standards(self, student_dir):
        pass


    def grade_includes(self, student_dir):
        pass


    def grade_error_and_doc(self, student_dir):
        total_penalty = 0
        grading_msg = []
        for root, _, fnames in os.walk(student_dir):
            for fname in fnames:
                extension = os.path.splitext(fname)[1][1:]
                if extension in ["cpp", "h"]:
                    p = subprocess.Popen([self.command, os.path.join(root, fname)] + self.extra_args, 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output = p.communicate()[0]
                    osplit = output.decode('utf-8').split('\n')
                    for line in osplit:
                        m = self.clang_msg_re.match(line)
                        if m is not None and m.group('check') in self.marking_scheme:
                            grading_msg.append("Mistake:{0}".format(m.group('msg')))
                            grading_msg.append("File: {0}, Line: {1}, Column: {2}".format(m.group('filepath'), m.group('line'), m.group('column')))
                            grading_msg.append("Penalty: %i\n" % self.marking_scheme[m.group('check')])
                            total_penalty += self.marking_scheme[m.group('check')]
        grading_msg.append("Total penalty: %i\n" % total_penalty)
        return '\n'.join(grading_msg)


def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

if __name__ == '__main__':
    main()
