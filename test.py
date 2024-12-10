import unittest
from ClassNameValidator import ClassNameValidator
from ReportLengthValidator import ReportLengthValidator
from bot import min_report_symbols


class EnteredClassTest(unittest.TestCase):

    def test_more_letters(self):
        typed_class = str('123')
        res = ClassNameValidator.validate(typed_class)
        error_msg = str(typed_class) + " is not False"
        self.assertFalse(res, error_msg)

    def test_first_digit_is_zero(self):
        typed_class = str('01')
        res = ClassNameValidator.validate(typed_class)
        error_msg = str(typed_class) + " is not False"
        self.assertFalse(res, error_msg)
    
    def test_correct_class_with_letter(self):
        typed_class = str('12a')
        res = ClassNameValidator.validate(typed_class)
        error_msg = str(typed_class) + " is not True"
        self.assertTrue(res, error_msg)

    def test_correct_class_without_letter(self):
        typed_class = str('12')
        res = ClassNameValidator.validate(typed_class)
        error_msg = str(typed_class) + " is not True"
        self.assertTrue(res, error_msg)

    def test_only_letters(self):
        typed_class = str('abc')
        res = ClassNameValidator.validate(typed_class)
        error_msg = str(typed_class) + " is not False"
        self.assertFalse(res, error_msg)
    
    def test_digit_with_two_letters(self):
        typed_class = str('9ab')
        res = ClassNameValidator.validate(typed_class)
        error_msg = str(typed_class) + " is not False"
        self.assertFalse(res, error_msg)   

    def test_incorrect_digits_with_one_letter(self):
        typed_class = str('14b')
        res = ClassNameValidator.validate(typed_class)
        error_msg = str(typed_class) + " is not False"
        self.assertFalse(res, error_msg)         


class CheckReportMinSymbolsTest(unittest.TestCase):

    def test_report_more_than_min_report_symbols(self):
        msg = 'a' * (min_report_symbols + 1)
        res = ReportLengthValidator.validate(msg, min_report_symbols)
        error_msg = str(msg) + " is not True"
        self.assertTrue(res, error_msg) 
    
    def test_report_with_exactly_min_report_symbols(self):
        msg = 'a' * min_report_symbols
        res = ReportLengthValidator.validate(msg, min_report_symbols)
        error_msg = str(msg) + " is not True"
        self.assertTrue(res, error_msg) 

    def test_report_less_than_min_report_symbols(self):
        msg = 'a' * (min_report_symbols - 1)
        res = ReportLengthValidator.validate(msg, min_report_symbols)
        error_msg = str(msg) + " is not True"
        self.assertFalse(res, error_msg) 


if __name__ == '__main__':
    unittest.main()