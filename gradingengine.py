import argparse
import os
import re
import subprocess


class GradingEngine:
    def __init__(self):
        self.command = "clang-tidy"
        self.extra_args = ["--","-Weverything"]
        self.marking_scheme = {}
        self.clang_msg_re = re.compile("(?P<filepath>.*):(?P<line>[0-9]+):(?P<column>[0-9]+): warning: (?P<msg>.*)\[(?P<check>.*)\]")


    def set_marking_scheme(self, marking_scheme):
        for err in marking_scheme.values():
            if err.is_enabled:
                self.marking_scheme[err.check] = err.penalty


    def execute_program(exe, data_dir):
        results = []
        for dirpath, _, filename in os.walk(data_dir):
            p = subprocess.Popen([exe, os.path.join(dirpath, filename)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = p.communicate()[0]
            results.append(output.decode('utf-8'))


    def grade_all(self, hw_root_dir, res_dir, correct_exe, data_dir):
        # Prepare expected results
        expected_results = self.execute_program(correct_exe, data_dir)

        # Grade all student directories
        if os.path.isdir(hw_root_dir):
            for student_dir in os.listdir(hw_root_dir):
                complete_student_dir = os.path.join(hw_root_dir, student_dir)
                if os.path.isdir(complete_student_dir):
                    student_result = self.grade_student(complete_student_dir, data_dir, expected_results)
                    with open('%s/%s.txt' % (res_dir, student_dir), 'w+') as student_res_file:
                        student_res_file.write(student_result)


    def grade_student(self, student_dir, data_dir, expected_results):
        # Get the student sources
        sources = []
        for dirpath, _, filename in os.walk(student_dir):
            if filename.endswith('.h') or filename.endswith('.cpp'):
                sources.append(os.path.join(dirpath, filename))

        # Grade student
        student_res = self.grade_correctness(sources, data_dir, expected_results)
        student_res = student_res + self.grade_includes(sources)
        student_res = student_res + self.grade_coding_standards(sources)
        student_res = student_res + self.grade_error_and_doc(sources)
        return student_res


    def grade_correctness(self, sources, data_dir, expected_results):
        # Compile the student's sources
        subprocess.Popen(['g++', sources], stdout=subprocess.PIPE, stderr = subprocess.PIPE)

        # Check that an executable was actually produced
        student_exe = os.path.join(os.curdir, 'a.out')
        if not os.isfile(student_exe):
            return "Couldn't compile the homework sources"

        student_results = self.execute_program(student_exe, data_dir)
        errors = []
        for student_res, expected_res in zip(student_results, expected_results):
            if not student_res == expected_res:
                errors.append('Incorrect output')
    
        return errors


    def grade_coding_standards(self, sources):
        pass


    def grade_includes(self, sources):
        pass


    def grade_error_and_doc(self, sources):
        total_penalty = 0
        grading_msg = []
        for source in sources:
            p = subprocess.Popen([self.command, os.path.join(source)] + self.extra_args, 
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
