#!/usr/bin/env python

__version__ = "0.0.1"

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from classify_clause import matching_rate

import docx2txt
import string
import re
import pdb
import numpy as np 
import nltk

class FileReader:
    def __init__(self):
        pass

    clause = ["0", "0)", "", "", "(0)", "", ""]

    ascii_upper_letters = string.ascii_uppercase
    ascii_letters = string.ascii_lowercase

    headers_only = True
    file_path = ""
    to_find = ""

    result_set = list()

    def find(self, path=None, to_find=None, headers_only=True):
        if(path[-3:]!="pdf"):
            text = docx2txt.process(path)
        else:
            text = self.convert(path)
        result_st = list()
        result_st = self.find_with(text, to_find, headers_only)
        return result_st

    def find_with(self, text=None, to_find=None, headers_only=True):
        self.clause = ["0", "0)", "", "", "(0)", "", ""]
        self.result_set = list()

        for blines in text.splitlines():
            blines = blines.replace(':','.')
            for line in nltk.sent_tokenize(blines):
                # pdb.set_trace()
                try:
                    l = self.decode_encode(line)
                except:
                    l = line.encode('utf-8').strip()
                    l = self.decode_encode(l)
                #print("----------#########----------", l)
                number_clause = re.findall('^([0-9]{1,2}\))', l)
                if (len(number_clause) > 0 and (
                        int(self.clause[1][:-1]) + 1 == int(number_clause[0][:-1]) or (int(number_clause[0][:-1]) == 1) and int(
                    self.clause[1][:-1]) != 1)):
                    self.clause[1] = number_clause[0]
                    # self.clause[2] = ""
                    self.clause[3] = ""
                    self.clause[4] = "(0)"
                    self.clause[5] = ""
                    self.clause[6] = ""
                    l = l.replace(number_clause[0], "")

                number_clause = re.findall('^([0-9.]{2,3})', l)
                if (len(number_clause) > 0 and number_clause[0].strip()[-1:] == "." and (
                        int(self.clause[0]) + 1 == int(number_clause[0].replace(".", "").strip()) or (
                        int(number_clause[0].replace(".", "").strip()) == 1) and int(self.clause[0]) != 1)):
                    self.clause[0] = number_clause[0].replace(".", "").strip()
                    self.clause[1] = "0)"
                    self.clause[2] = ""
                    self.clause[3] = ""
                    self.clause[4] = "(0)"
                    self.clause[5] = ""
                    self.clause[6] = ""
                    l = l.replace(number_clause[0], "")
                alpha_clause = re.findall("^[a-z]{1}\.", l)
                if (len(alpha_clause) > 0):
                    self.clause[2] = alpha_clause[0]
                    self.clause[3] = ""
                    # self.clause[4] = "(0)"
                    self.clause[5] = ""
                    self.clause[6] = ""
                    l = l.replace(alpha_clause[0], "")
                    alpha_clause
                alpha_clause = re.findall("^\([a-z]{1}\)", l)
                if (len(alpha_clause) == 0):
                   alpha_clause = re.findall(r" {1}[a-z]{1}\.| {1}[a-z]{1}\)", l)
                if (len(alpha_clause) > 0):
                    if (alpha_clause[0].replace("(", "")[:-1] == "(v)" and self.clause[2] != "(u)"):
                        self.clause[6] = alpha_clause[0].replace("(", "")[:-1]
                        l = l.replace(alpha_clause[0], "")
                    else:
                        if (self.ascii_letters.find(alpha_clause[0].replace("(", "")[:-1]) == 0 and self.clause[2] == ""):
                            self.clause[2] = alpha_clause[0]
                            self.clause[3] = ""
                            # self.clause[4] = "(0)"
                            self.clause[5] = ""
                            self.clause[6] = ""
                            l = l.replace(alpha_clause[0], "")
                        elif ((self.ascii_letters.find(alpha_clause[0].strip().replace(".", "")[:-1]) == 0) or (self.ascii_letters.find(alpha_clause[0].strip().replace(")", "")[:-1]) == 0)):
                            if(self.clause[2] != "" and self.clause[3] == ""):
                              self.clause[3] = alpha_clause[0].strip()
                            else:
                              self.clause[2] = alpha_clause[0].strip()
                              self.clause[3] = ""
                            # self.clause[4] = "(0)"
                            self.clause[5] = ""
                            self.clause[6] = ""
                            l = l.replace(alpha_clause[0], "")
                        else:
                            pos = self.ascii_letters.find(self.clause[2].replace("(", "")[:-1])
                            if (pos + 1 == self.ascii_letters.find(alpha_clause[0].replace("(", "")[:-1])):
                                self.clause[2] = alpha_clause[0]
                                self.clause[3] = ""
                                # self.clause[4] = "(0)"
                                self.clause[5] = ""
                                self.clause[6] = ""
                                l = l.replace(alpha_clause[0], "")
                number_clause = re.findall('^(\([0-9]{1,2}\))', l)
                if (len(number_clause) > 0 and (
                        int(self.clause[4].replace("(", "")[:-1]) + 1 == int(number_clause[0].strip().replace("(", "")[:-1]) or (
                        int(number_clause[0].strip().replace("(", "")[:-1]) == 1) and int(
                        self.clause[4].replace("(", "")[:-1]) != 1)):
                    self.clause[4] = number_clause[0]
                    self.clause[5] = ""
                    self.clause[6] = ""
                    l = l.replace(number_clause[0], "")

                # second case for sublcauses in same line as . (0)
                number_clause = re.findall("\.\s\([0-9]\)", l)
                if(len(number_clause) > 0 and (
                        int(self.clause[4].replace("(", "")[:-1]) + 1 == 1)):
                    self.clause[4] = number_clause[0]
                    self.clause[5] = ""
                    self.clause[6] = ""
                    l = l.replace(number_clause[0], "")

                alpha_clause = re.findall("^\([A-Z]{1}\)|[A-Z]{1}\.", l)
                if (len(alpha_clause) > 0):
                    if (self.ascii_upper_letters.find(alpha_clause[0].replace("(", "")[:-1]) == 0 and self.clause[5] == ""):
                        self.clause[5] = alpha_clause[0]
                        # self.clause[6] = ""
                        parent_number_before_alpha_clause = re.findall('[0-9]{1,2}\.|[0-9]{2,3}\.', l)
                        self.clause[3] = ""
                        l = l.replace(alpha_clause[0], "")
                    else:
                        pos = self.ascii_upper_letters.find(self.clause[5].replace("(", "")[:-1])
                        if (pos + 1 == self.ascii_upper_letters.find(alpha_clause[0].replace("(", "")[:-1]) and self.clause[6] == ""):
                            self.clause[5] = alpha_clause[0]
                            # self.clause[6] = ""
                            self.clause[3] = ""
                            l = l.replace(alpha_clause[0], "")
                roman_clause = re.findall("\(x{0,3}(?:v?i{0,3}|i[vx])\)", l)
                if (len(roman_clause) > 0):
                    for x in range(len(roman_clause)):
                        # if(l.find(to_find[x]) != -1)
                        reg1= r"%s" % roman_clause[x]
                        backward_match = l.split(reg1)[1]
                        if(backward_match.find(to_find[0]) != -1):
                          self.clause[6] = roman_clause[x]
                          l = l.replace(roman_clause[x], "")

                for x in range(len(to_find)):
                    l = string.lower(l)

                    try:
                        to_find[x] = to_find[x].decode('cp1250').encode('ascii', 'ignore').strip()
                    except:
                        to_find[x] = to_find[x].decode('CP1252').encode('ascii', 'ignore')
                    to_find[x] = to_find[x].replace("'", "")
                    to_find[x] = string.lower(to_find[x])
                    if(headers_only):
                        if (str(l.strip())[:len(to_find[x].strip())] == to_find[x].strip()):
                            sent_tokenize_list = re.split(r'[.,]', l.strip())
                            self.result_set.append([self.printer(), sent_tokenize_list[0]])
                    else:
                        if(l.find(to_find[x]) != -1):
                            self.result_set.append(self.printer())

        return np.unique(self.result_set)

    def printer(self):
        clause_value = ""
        if self.clause[0] != "0":
            clause_value += self.clause[0] + ""
        if self.clause[4] != "(0)":
            clause_value += self.clause[4] + ""
        if self.clause[2] != "":
            clause_value += self.clause[2] + ""
        if self.clause[1] != "0)":
            clause_value += self.clause[1] + ""
        if self.clause[3] != "":
            clause_value += self.clause[3] + ""
        if self.clause[5] != "":
            clause_value += self.clause[5] + ""
        if self.clause[6] != "":
            clause_value += self.clause[6]
        return clause_value

    def convert(self, fname, pages=None):
        print "reading",
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)

        infile = file(fname, 'rb', )
        for page in PDFPage.get_pages(infile, pagenums):
            print ".",
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
        print " done\n"
        return text

    def decode_encode(self, line):
        try:
            return line.decode('cp1250').encode('ascii', 'ignore').strip()
        except:
            return line.decode('CP1252').encode('ascii', 'ignore')

