from __future__ import absolute_import, unicode_literals

from django import template


register = template.Library()


@register.filter
def group_by_tree(iterable):
    """
    Group pages of two navigation levels. Usage example::

        {% load feincms3_pages %}

        <nav class="nav-main">
        {% menu "main" level=1 depth=2 tree_id=page.tree_id as pages %}
        {% for main, children in pages|group_by_tree %}
          {% is_descendant_of page main include_self=True as active %}
          <a {% if active %}class="active"{% endif %}
             href="{{ main.get_absolute_url }}"{{ main.title }}</a>
            {% if children %}
            <nav>
              {% for child in children %}
                {% is_descendant_of page child include_self=True as active %}
                <a {% if active %}class="active"{% endif %}
                   href="{{ child.get_absolute_url }}"{{ child.title }}</a>
              {% endfor %}
            </nav>
          {% endif %}
        {% endfor %}
        </nav>
    """

    parent = None
    children = []
    level = -1

    for element in iterable:
        if parent is None or element.level == level:
            if parent:
                yield parent, children
                parent = None
                children = []

            parent = element
            level = element.level
        else:
            children.append(element)

    if parent:
        yield parent, children


@register.simple_tag
def is_descendant_of(node1, node2, include_self=False):
    """
    Returns whether the first argument is a descendant of the second argument.

    The recommended usage is documented below for the {% menu %} template tag.
    """
    return node1.is_descendant_of(node2, include_self=include_self)


@register.simple_tag(takes_context=True)
# def menu(menu, *, level=0, depth=1, **kwargs):
def menu(context, menu, level=0, depth=1, **kwargs):  # PY2 :-(
    """
    This tag expects the ``page`` variable to contain the page we're on
    currently. The active pages are fetched using ``.objects.active()`` and
    filtered further according to the arguments passed to the tag.

    Usage example::

        {% load feincms3_pages %}

        {% menu 'meta' as meta_nav %}
        <nav>
        {% for p in meta_nav %}
          {% is_descendant_of page p include_self=True as active %}
          <a href="{{ p.get_absolute_url }}" {% if active %}class="active">
             {{ p.title }}
          </a>
        {% endfor %}
        </nav>
    """

    return context['page'].__class__.objects.active().filter(
        menu=menu,
        level__range=[level, level + depth - 1],
        **kwargs
    )
