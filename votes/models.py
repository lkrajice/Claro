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

    class Meta:
        db_table = "Class"


class Pin(models.Model):
    """
    Store generated user's pins

    Pins are temporary
    """
    pin = models.CharField(max_length=32, unique=False, help_text="Temporary pin for specific user")

    class Meta:
        db_table = "Pin"


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

    class Meta:
        db_table = "Student"


class Election(models.Model):
    """
    Election grouping up election rounds

    This object is created by administrator
    """
    title = models.CharField(max_length=100, help_text="Title at the main page")

    class Meta:
        db_table = "Election"


class RoundType(models.Model):
    """
    Enumerate for vote
    """
    name = models.CharField(max_length=20, unique=True, help_text="type")

    class Meta:
        db_table = "RoundType"


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

    class Meta:
        db_table = "Round"


class Candidate(models.Model):
    """
    Link to student that have been selected to candidate by class
    """
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    round_id = models.ForeignKey(Round, on_delete=models.PROTECT)

    votes = models.PositiveSmallIntegerField(help_text="Year when election took place")
    accepted = models.BooleanField()

    class Meta:
        db_table = "Candidate"


class Vote(models.Model):
    """
    Represents one vote from student

    After election have ended, votes should be deleted to keep anonymity.
    """
    voting_id = models.ForeignKey(Round, on_delete=models.PROTECT)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    vote_for = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    class Meta:
        db_table = "Vote"
