from django import template

register = template.Library()


@register.filter(name='is_user_type')
def is_user_type(user, required_type):
    return user.groups.filter(name=required_type).exists()
