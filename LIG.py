import csv
import os


def supported_langs_file():
    if os.path.exists("Tesseract_Langs.txt"):
        return "Tesseract_Langs.txt"  
    else:
        print("The expected supported languages file is not in the directory. "
              "Tesseract_Langs.txt is available in the github repo")
        return None


def get_language_from_code(code):
  
    file = supported_langs_file()

    l_dict = {}
    with open(file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for el in reader:
            key = el[0]
            name = el[1]
            l_dict[key] = name

    try:
        return l_dict[code]
    except KeyError: 
        return code


def show_codes():
    
    file = supported_langs_file()

    with open(file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        print("{:<20s}{:<40s}".format("CODE", "LANGUAGE"))
        for el in reader:
            print("{:<20s}{:<40s}".format(el[0], el[1]))


def language_string(language):
    
    if language is not None:  
        name_list = []
        codes = language.split('+')  
        for language in codes:
            name = get_language_from_code(language)
            name_list.append(name)
        lang_name = ', '.join(name_list)

    else:  
        lang_name = 'English'

    return lang_name
