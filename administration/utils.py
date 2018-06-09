"""
Contains parser
"""
import os

from .models import Student, Class, Pin
import random
NUMBERS = "0123456789"
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPECIAL = ",.-ůú)/*-+"


class StudentDataFileParser:
    """
        StudentDataFilePArser
        This class parses data file which is gettable by method get_data

        Params:
            file_path (String)- path to file
            text_file_delimeter (Stringú)- delimeter for file, default is ;

        Attributes:
            file_name (String)- name of the file
            file_extension (String)- extension of file
            data (List)- list of lists filled with data
    """
    delimeter = ';'

    @classmethod
    def proccess_file(cls, filepath):
        """
        Proccess file with students
        """
        cls.wipedb()

        students = []
        classes = set()
        with open(filepath, 'r') as f:
            for line in f.readlines():
                data = line.strip().split(cls.delimeter)

                name = '{name} {lastname}'.format(name=data[0], lastname=data[1])
                userid = '{lastname}.{name}'.format(name=data[0].lower(), lastname=data[1].lower())
                student = {'class_id': None,
                           'pin_id': None,
                           'name': name,
                           'email': data[3],
                           'profile_image': userid,
                           '#class': data[2]}  # temporary attribute

                classes.add(data[2])
                students.append(student)

        Class.objects.bulk_create([Class(shortname=c, classtype=c[0]) for c in classes])
        class_dict = {c.shortname: c for c in Class.objects.all()}
        for i in range(len(students)):
            students[i]['class_id'] = class_dict[students[i].pop('#class')]

        Student.objects.bulk_create([Student(**student) for student in students])

    @staticmethod
    def wipedb():
        """
        Wipe tables
        """
        Student.objects.all().delete()
        Class.objects.all().delete()
        Pin.objects.all().delete()

    def generate_pin(self, pin_length=32, source=NUMBERS + ALPHABET + SPECIAL):
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
            chars.append(random.choice(source))
        final = "".join(chars)
        return final

    def get_data(self):
        """
            Description:
                Method returns data parsed by other methods
            Returns:
                data (list)- list of lists with data from source file
        """
        return self.data
