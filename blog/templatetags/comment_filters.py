from django import template

register = template.Library()

@register.filter
def approved_comments(comments):
    return comments.filter(is_approved=True)

@register.filter
def pending_comments(comments):
    return comments.filter(is_approved=False)

@register.filter
def count_approved(comments):
    return comments.filter(is_approved=True).count()

@register.filter
def count_pending(comments):
    return comments.filter(is_approved=False).count()