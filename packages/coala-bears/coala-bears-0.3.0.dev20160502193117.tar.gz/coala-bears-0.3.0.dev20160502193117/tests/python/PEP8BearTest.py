from queue import Queue

from bears.python.PEP8Bear import PEP8Bear
from tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class PEP8BearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.section.append(Setting('max_line_length', '80'))
        self.uut = PEP8Bear(self.section, Queue())

    def test_valid(self):
        self.check_validity(self.uut, ["import sys"])
        self.check_validity(self.uut, ["a = 1 + 1"])

    def test_line_length(self):
        self.check_validity(self.uut, ["a = 1 + 1 + 1 + 1 + 1 + 1 + 1"])
        self.section.append(Setting('max_line_length', '10'))
        self.check_validity(self.uut,
                            ["a = 1 + 1 + 1 + 1 + 1 + 1 + 1"],
                            valid=False)

    def test_indent_level(self):
        test_code = ['def func():\n',
                     '    pass\n']
        self.check_validity(self.uut, test_code)

        self.section.append(Setting('tab_width', '2'))
        self.check_validity(self.uut, test_code, valid=False)
        self.check_validity(self.uut, ['def func():\n', '  pass\n'])

    def test_disable_warnings(self):
        test_code = ['def func():\n',
                     '    pass\n',
                     'def func2():\n',
                     '    pass\n']
        self.check_validity(self.uut, test_code, valid=False)

        self.section.append(Setting('pep_ignore', 'E302'))
        self.check_validity(self.uut, test_code)

    def test_invalid(self):
        self.check_validity(self.uut, [""], valid=False)
        self.check_validity(self.uut, ["a=1+1"], valid=False)
