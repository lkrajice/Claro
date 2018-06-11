# -*- coding: utf-8 -*-
"""Define db model for parlament application"""
import datetime
import math

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

    @property
    def compare(self):
        """
        Compare round's start and end to current time

        Returns:
            (int): -1 if round took place, 0 if active, 1 if round will become active
        """
        now = datetime.datetime.now()
        start_in_datetime = datetime.datetime.combine(self.start, datetime.datetime.min.time())
        end_in_datetime = datetime.datetime.combine(self.end, datetime.datetime.max.time())
        if now < start_in_datetime:
            return 1;
        if end_in_datetime < now:
            return -1;
        return 0;

    @property
    def percent(self):
        """
        Return progress towards end of the round
        """
        now = datetime.datetime.now()
        start_in_datetime = datetime.datetime.combine(self.start, datetime.datetime.min.time())
        from_start = (now - start_in_datetime).total_seconds()
        start_to_end = (self.end - self.start).total_seconds()

        if from_start < 0:
            return 0
        if start_to_end == 0:
            start_to_end = 24 * 60 * 60

        return min(100, int(from_start // (start_to_end / 100)))


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


class ElectionController:

    def __init__(self):
        self.is_active_election = self.is_active_election()
        self.all_election_active_rounds = [Round.objects.all()[0], Round.objects.all()[1], Round.objects.all()[2]]
        self.first_round = Round.objects.all()[0]
        self.second_round = Round.objects.all()[1]
        self.third_round = Round.objects.all()[2]
        self.all_active_rounds = self.fill_all_active_rounds()
        self.active_election = self.fill_active_election()
        self.active_round = self.fill_active_round()
        self.active_round_number = self.fill_round_number()
        self.all_rounds = Round.objects.all()
        self.all_non_active_rounds = self.fill_all_not_active_rounds()

    def is_active_election(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        res = 0
        r = [Round.objects.all()[0], Round.objects.all()[1], Round.objects.all()[2]]
        for round in r:
            if round.end.strftime("%Y-%m-%d") < today:
                res +=1
        if res == 3:
            print("NN")
            return False
        print("YY")
        return True

    def fill_all_active_rounds(self):
        newlist = []
        list = self.all_election_active_rounds
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        for round in list:
            if round.start.strftime("%Y-%m-%d") <= today and round.end.strftime("%Y-%m-%d") >= today:
               newlist.append(round)
        return newlist

    def fill_active_election(self):
        return self.all_active_rounds[0].election_id

    def fill_active_round(self):
        return self.all_active_rounds[0]

    def fill_round_number(self):
        return self.all_active_rounds[0].round_number

    def fill_all_not_active_rounds(self):
        list = []
        for round in self.all_rounds:
            list.append(round)
        del list[0]
        del list[1]
        del list[2]
        return list
