from django import template
from django.db.models import Count

from votes.models import Vote

register = template.Library()


@register.inclusion_tag('student_board.html')
def students_board(students, e_round, disabled, reason):
    context = {'students': None,
               'disabled': disabled,
               'reason': reason}

    # Get number of points for each student
    votes_count = Vote.objects\
        .all()\
        .filter(vote_for__round_id=e_round, vote_for__student_id__in=students)\
        .values('vote_for__student_id__id')\
        .annotate(total=Count('id'))
    votes_dict = {d['vote_for__student_id__id']: d['total'] for d in votes_count}

    for student in students:
        student.total_votes = votes_dict.get(student.id, 0)
    context['students'] = sorted(students, key=lambda x: x.total_votes, reverse=True)

    return context
