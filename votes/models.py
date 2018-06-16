# -*- coding: utf-8 -*-
"""Define db model for parlament application"""
import datetime

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


class Election(models.Model):
    """
    Election grouping up election rounds

    This object is created by administrator
    """
    title = models.CharField(max_length=100, help_text="Title at the main page")

    class Meta:
        db_table = "Election"

    @property
    def get_rounds(self):
        return Round.objects.all().filter(election_id=self)

    @property
    def get_first_round(self):
        return Round.objects.all().get(election_id=self, round_number=1)

    @property
    def get_second_round(self):
        return Round.objects.all().get(election_id=self, round_number=2)

    @property
    def get_third_round(self):
        return Round.objects.all().get(election_id=self, round_number=3)


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

    @property
    def convert_start_time(self):
        return datetime.datetime.strftime(self.start, "%Y-%m-%d")

    @property
    def convert_end_time(self):
        return datetime.datetime.strftime(self.end, "%Y-%m-%d")


class Student(models.Model):
    """
    Store students

    When student is updated, new entry is added to the database and `active` of old one is set to
    False & `old` is set to True.
    """
    class_id = models.ForeignKey(Class, on_delete=models.PROTECT)

    name = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image = models.FileField(upload_to=user_image_name, help_text='Profile image')

    class Meta:
        db_table = "Student"


class Pin(models.Model):
    """
    Store generated user's pins

    Pins are temporary
    """
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE)
    pin = models.CharField(max_length=32, unique=False, help_text="Temporary pin for specific user")

    class Meta:
        db_table = "Pin"


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
