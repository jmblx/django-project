from django import template

from memes.models import Category

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('memsite/list_categories.html', takes_context=True)
def show_categories(context):

    cats = Category.objects.all()
    cat_selected = context['cat_selected']
    auth = context['auth']

    return {"categories": cats, "cat_selected": cat_selected, 'auth': auth}

