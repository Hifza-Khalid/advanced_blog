from .models import Category

def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}

def user_info_processor(request):
    context = {}
    if request.user.is_authenticated:
        context['is_author'] = request.user.groups.filter(name='Authors').exists() or request.user.is_staff
        context['user_groups'] = list(request.user.groups.values_list('name', flat=True))
    return context