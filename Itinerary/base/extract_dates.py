import os
from PyPDF2 import PdfReader
import re

directory = os.path.dirname(__file__)
directory = os.path.dirname(directory)
directory = os.path.dirname(directory)
pdf_file_name = 'Bits Holidays 23-24.pdf'
file_path = os.path.join(directory, pdf_file_name)

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        words = []  # List to store words
        for page_num in range(num_pages):
            text = pdf_reader.pages[page_num].extract_text()
            # Split text into words using regular expression
            page_words = re.findall(r'\b\w+\b', text)
            words.extend(page_words)
        return words

pdf_words = read_pdf(file_path)
for i in range(0, len(pdf_words)):
    if pdf_words[i] == 'First':
        pdf_words = pdf_words[i:]
        break

holiday_dict = {}

semester_change_number = 0

for i in range(0, len(pdf_words)):
    if pdf_words[i] == "Second" and pdf_words[i + 1] == "Semester":
        semester_change_number = i
        break
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
for i in range(len(pdf_words)):
    if pdf_words[i] in months:
        date = pdf_words[i] + ' ' + pdf_words[i + 1]
        if pdf_words[i+2] in ['M', 'T', 'W', 'Th', 'F', 'S', 'Su', 'TH']:
            day = pdf_words[i + 2]
            if (i + 3) < len(pdf_words) and pdf_words[i + 3] in ['to', '-']:
                if i + 4 in months:
                    date += ' ' + pdf_words[i + 3] + ' ' + pdf_words[i + 4] + ' ' + pdf_words[i + 5]
                    for j in range(i + 6, len(pdf_words)):
                        if pdf_words[j] == 'H' or pdf_words[j] == "Recess":
                            if i < semester_change_number:
                                date += ' ' + '2023'
                                holiday_dict[date] = "Vacation"
                            else:
                                date += ' ' + '2024'
                                holiday_dict[date] = "Vacation"
                            break
                        elif pdf_words[j] in months:
                            break
                else:
                    date += ' ' + pdf_words[i + 3] + ' ' + pdf_words[i + 4]
                for j in range(i + 5, len(pdf_words)):
                    if pdf_words[j] == 'H' or pdf_words[j] == "Recess":
                        if i < semester_change_number:
                            date += ' ' + '2023'
                            holiday_dict[date] = "Vacation" 
                        else:
                            date += ' ' + '2024'
                            holiday_dict[date] = "Vacation"
                        break
                    elif pdf_words[j] in months:
                        break
            elif (i + 3) < len(pdf_words) and pdf_words[i + 3] == "Summer" and pdf_words[i + 4] == "Vacation" and pdf_words[i + 5] == "begins":
                for j in range(i + 6, len(pdf_words)):
                    if pdf_words[j] == "Vacation" and pdf_words[j + 1] == "ends":
                        date += ' ' + "to" + ' ' + pdf_words[j - 4] + ' ' + pdf_words[j - 3]
                        if i < semester_change_number:
                            date += ' ' + '2023'
                            holiday_dict[date] = "Vacation"
                        else:
                            date += ' ' + '2024'
                            holiday_dict[date] = "Vacation"
                        break
            else:
                for j in range(i + 3, len(pdf_words)):
                    if pdf_words[j] == 'H':
                        if i < semester_change_number:
                            date += ' ' + '2023'
                            holiday_dict[date] = day
                        else:
                            date += ' ' + '2024'
                            holiday_dict[date] = day
                        break
                    elif pdf_words[j] in months:
                        break