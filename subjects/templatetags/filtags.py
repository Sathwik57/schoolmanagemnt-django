from django import template

from subjects.models import GradedAssignment
# from .models import Question

register = template.Library()


@register.simple_tag()
def option(ques,answer):
	op = 'option' + str(answer)
	return eval(f'ques.{op}')


@register.simple_tag(takes_context=True)
def is_user(context,username):
	user = context['request'].user.username
	return username == user

@register.simple_tag(takes_context=True)
def is_graded(context,quiz):
	student = context['request'].user.student
	try:
		grade =	GradedAssignment.objects.get( assignment = quiz, student = student ).grade
		return grade
	except:
		return None


