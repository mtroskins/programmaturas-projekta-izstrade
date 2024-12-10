import csv
from datetime import datetime

class CsvLogger:
    @staticmethod
    def log(report_text : str, cl : str):
        if cl == '':
            cl = 'ANON'
        report_text = report_text.replace('\n', '. ')
        with open('ReportLog.csv', mode='a', newline='') as report_file:
        # Create a CSV writer object
            writer = csv.writer(report_file, delimiter='|')
            current = datetime.now() #  Get the current date and time as a datetime object
            current_str = current.strftime("%d-%m-%Y %H:%M:%S") #  Format it as a string
            row = (current_str, report_text, cl)
            writer.writerow(row)