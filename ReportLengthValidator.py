class ReportLengthValidator:
    @staticmethod
    def validate(string : str, min_report_symbols : int) -> bool:
        if len(string) >= min_report_symbols:
            return True
        else:
            return False