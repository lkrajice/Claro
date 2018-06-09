from django.db import models

# Create your models here.
import os
import random as r
# -*- coding: utf-8 -*-
"""Define db model for parlament application"""
from django.db import models


class Class(models.Model):
    """
    Store metadata of every class at school

    Values in this table are constant, they should never be removed, but new classes may be added.
    """
    shortname = models.CharField(max_length=10, unique=True, help_text="Abbreviation of a class")
    classtype = models.CharField(max_length=3, unique=False, help_text="Class type: V, S, I or K...")


class Pin(models.Model):
    """
    Store generated user's pins

    Pins are temporary
    """
    pin = models.CharField(max_length=32, unique=False, help_text="Temporary pin for specific user")


def user_image_name(instance, filename):
    """
    Function returning the filename for profile image of user

    Method is called automatically. File is saved under MEDIA_ROOT/

    Args:
        instance: instance of Student
        filename: filename that was given by django before calling the method

    Returns:
        filename in format 'profile_<id>'
    """
    return 'profile_{userid}'.format(userid=instance.id)


class Student(models.Model):
    """
    Store students

    When student is updated, new entry is added to the database and `active` of old one is set to
    False & `old` is set to True.
    """
    class_id = models.ForeignKey(Class, on_delete=models.PROTECT)
    pin_id = models.ForeignKey(Pin, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image = models.FileField(upload_to=user_image_name, help_text='Profile image')


class Election(models.Model):
    """
    Election grouping up election rounds

    This object is created by administrator
    """
    title = models.CharField(max_length=100, help_text="Title at the main page")


class RoundType(models.Model):
    """
    Enumerate for vote
    """
    name = models.CharField(max_length=20, unique=True, help_text="type")


class Round(models.Model):
    """
    Store one round of and election

    This object is created automatically and partly modified by administrator
    """
    election_id = models.ForeignKey(Election, on_delete=models.PROTECT)
    type_id = models.ForeignKey(RoundType, on_delete=models.PROTECT)

    round_number = models.PositiveSmallIntegerField(help_text="Which round of voting is it.")
    start = models.DateField()
    end = models.DateField()


class Candidate(models.Model):
    """
    Link to student that have been selected to candidate by class
    """
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    round_id = models.ForeignKey(Round, on_delete=models.PROTECT)

    votes = models.PositiveSmallIntegerField(help_text="Year when election took place")
    accepted = models.BooleanField()


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
        self.file_name, self.file_extension = self.get_file_properly(file_path)
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
        print("Koncovka je" + file_extension)
        print("jemno je" + filename)
        if file_extension != ".txt":
            raise ValueError("This file extension is not supported, supported extension is txt")
        return filename, file_extension

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
        pass
