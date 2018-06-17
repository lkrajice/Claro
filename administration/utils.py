# -*- coding: utf-8 -*-
"""
Contains parser
"""
import random

from string import digits

from votes.models import Student, Class, Pin, RoundType


def generate_pin(pin_length=16, source=digits):
    """
        Description:
            Method that created random pin
        Params:
            pin_length (int)- desired length of pin
            source (String)- string of chars that pin will be created from
        Returns:
            final (String)- created pin
    """
    return ''.join(random.choice(source) for _ in range(pin_length))


class StudentDataFileParser:
    """
        Parse students, wipe database and start election

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
                           'name': name,
                           'email': data[3],
                           'profile_image': userid,
                           '#class': data[2]}  # temporary attribute

                classes.add(data[2])
                students.append(student)

        Class.objects.bulk_create([Class(shortname=c, classtype=c[0]+'*') for c in classes])
        class_dict = {c.shortname: c for c in Class.objects.all()}

        for i in range(len(students)):
            students[i]['class_id'] = class_dict[students[i].pop('#class')]

        Student.objects.bulk_create([Student(**student) for student in students])

        # init RoundType
        types = RoundType.objects.all()
        if len(types) == 0:
            RoundType.objects.bulk_create(
                [RoundType(name='nomination'), RoundType(name='election')])

    @staticmethod
    def wipedb():
        """
        Wipe tables
        """
        Student.objects.all().delete()
        Class.objects.all().delete()
        Pin.objects.all().delete()

    def get_data(self):
        """
            Description:
                Method returns data parsed by other methods
            Returns:
                data (list)- list of lists with data from source file
        """
        return self.data


class MessageToPage:
    def __init__(self, message_type, message_bold, message_text, message_vars=""):
        self.message_type = message_type
        self.message_bold = message_bold
        self.message_text = message_text
        self.message_vars = message_vars
