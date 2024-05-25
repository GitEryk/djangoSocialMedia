from django import template
from images.models import Image

register = template.Library()


@register.inclusion_tag("images/image/ranking.html")
def show_most_liked():
    most_liked = Image.objects.all().order_by('-total_likes')[:10]
    return {'most_liked': most_liked}
