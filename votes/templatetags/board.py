from django import template

register = template.Library()


@register.inclusion_tag('student_board.html')
def students_board(students, disabled, reason):
    context = {'students': students,
               'disabled': disabled,
               'reason': reason}
    return context
