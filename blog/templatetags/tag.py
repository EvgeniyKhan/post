from django import template

register = template.Library()


@register.filter(name="mymedia")
def mymedia(value):
    if value:
        return f"/media/{value}"
    return "Снимок экрана 2024-07-12 в 22.25.01.png"
