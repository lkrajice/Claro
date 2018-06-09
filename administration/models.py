from django.db import models

# Create your models here.
import os
import random as r

NUMBERS = "0123456789"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPECIAL = ",.-ůú)/*-+"


class StudentParser:
    """
        UltraMegaParser
        This class parses data file which is gettable by method get_data
        Params:
            file_path (String)- path to file
            text_file_delimeter (Stringú)- delimeter for file, default is ;
        Attributes:
            file_name (String)- name of the file
            file_extension (String)- extension of file
            data (List)- list of lists filled with data
    """
    def __init__(self, file_path, text_file_delimeter=";"):
        this_folder = os.pathdirname(os.path.abspath(__file__))
        my_file = os.path.join(this_folder, file_path)
        self.file_name, self.file_extension = self.get_file_properly(my_file)
        self.text_file_delimeter = text_file_delimeter
        self.data = []

        self.parse_txt()

    def get_file_properly(self, file_name):
        """
            Description:
                Method splits file path into file name and extension, checks if class can handle this extension
                and returns filname and file extension
            Params:
                filename (String)- path to file
            Returns:
                filename (String) - file name
                file_extension (String) - file extensions, example: .txt
        """
        filename, file_extension = os.path.splitext(file_name)
        if file_extension != ".txt":
            raise ValueError("This file extension is not supported, supported extension is txt")
        return filename, file_extension

    def generate_pin(self, pin_length=50, source=NUMBERS + ALPHABET + SPECIAL):
        """
            Description:
                Method creates 50 chars long pin
            Params:
                pin_length (int)- desired length of pin
                source (String)- string of chars that pin will be created from
            Returns:
                final (String)- created pin
        """
        chars = []
        for i in range(pin_length):
            chars.append(r.choice(source))
        final = "".join(chars)
        return final

    def parse_txt(self):
        """
            Description:
                Method parses text file and adds pin
        """
        with open(self.file_name+self.file_extension) as FileObj:
            for line in FileObj:
                line = line.rstrip('\n')
                line += self.generate_pin()
                a = line.split(self.text_file_delimeter)
                self.data.append(a)

    def get_data(self):
        """
            Description:
                Method returns data parsed by other methods
            Returns:
                data (list)- list of lists with data from source file
        """
        return self.data

class LoadDataToDatabase:
    def __init__(self, data):
        self.data = data

    def load(self):
        for data in self.data:
            for information in data:
                
