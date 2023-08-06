from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import activate, get_language, ugettext_lazy as _


class MenuMixin(models.Model):
    """
    The ``MenuMixin`` is most useful on pages where there are menus with
    differing content on a single page, for example the main navigation
    and a meta navigation (containing contact, imprint etc.)

    The page class should extend the menu mixin, and define a ``MENUS``
    variable describing the available menus::

        from django.utils.translation import ugettext_lazy as _
        from feincms3.mixins import MenuMixin
        from feincms3.pages import AbstractPage

        class Page(MenuMixin, AbstractPage):
            MENUS = (
                ('main', _('main navigation')),
                ('meta', _('meta navigation')),
            )

    The ``menu`` template tag may be used to fetch navigation entries
    from the template. See feincms3.templatetags.feincms3_pages.menu.
    """

    menu = models.CharField(
        _('menu'),
        max_length=20,
        blank=True,
    )

    class Meta:
        abstract = True


@receiver(signals.class_prepared)
def _fill_menu_choices(sender, **kwargs):
    if issubclass(sender, MenuMixin) and not sender._meta.abstract:
        field = sender._meta.get_field('menu')
        field.choices = sender.MENUS
        field.default = field.choices[0][0]


class TemplateMixin(models.Model):
    """
    It is sometimes useful to have different templates for CMS models such
    as pages, articles or anything comparable. The ``TemplateMixin``
    provides a ready-made solution for selecting django-content-editor
    ``Template`` instances through Django's administration interface::

        from django.utils.translation import ugettext_lazy as _
        from content_editor.models import Template, Region
        from feincms3.mixins import TemplateMixin
        from feincms3.pages import AbstractPage

        class Page(TemplateMixin, AbstractPage):
            TEMPLATES = [
                Template(
                    key='standard',
                    title=_('standard'),
                    template_name='pages/standard.html',
                    regions=(
                        Region(key='main', title=_('Main')),
                    ),
                ),
                Template(
                    key='with-sidebar',
                    title=_('with sidebar'),
                    template_name='pages/with-sidebar.html',
                    regions=(
                        Region(key='main', title=_('Main')),
                        Region(key='sidebar', title=_('Sidebar')),
                    ),
                ),
            ]

    The selected ``Template`` instance is available using the ``template``
    property. If the value in ``template_key`` does not match any template,
    ``None`` is returned instead. django-content-editor also requires a
    ``regions`` property for its editing interface; the property returns the
    regions list from the selected template.
    """

    template_key = models.CharField(_('template'), max_length=100)

    class Meta:
        abstract = True

    @property
    def template(self):
        return self.TEMPLATES_DICT.get(self.template_key)

    @property
    def regions(self):
        return self.template.regions if self.template else []


@receiver(signals.class_prepared)
def _fill_template_key_choices(sender, **kwargs):
    if issubclass(sender, TemplateMixin) and not sender._meta.abstract:
        field = sender._meta.get_field('template_key')
        field.choices = [
            (t.key, t.title) for t in sender.TEMPLATES
        ]
        field.default = sender.TEMPLATES[0].key
        sender.TEMPLATES_DICT = {t.key: t for t in sender.TEMPLATES}


class LanguageMixin(models.Model):
    """
    Pages may come in varying languages. ``LanguageMixin`` helps with that.
    It uses ``settings.LANGUAGES`` for the language selection, and sets the
    first language as default::

        from django.utils.translation import ugettext_lazy as _
        from feincms3.mixins import LanguageMixin
        from feincms3.pages import AbstractPage

        class Page(LanguageMixin, AbstractPage):
            pass

    The language itself is saved as ``language_code`` on the model. Also
    provided is a method ``activate_language`` which activates the selected
    language using ``django.utils.translation.activate`` and sets
    ``LANGUAGE_CODE`` on the request, the same things Django's
    ``LocaleMiddleware`` does::

        def page_detail(request, path):
            page = # Fetch the Page instance somehow
            page.activate_language(request)

    Note that this does not persist the language in the session or in a
    cookie. If you need this, you should use Django's
    ``django.views.i18n.set_language`` view.
    """

    language_code = models.CharField(
        _('language'),
        max_length=10,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGES[0][0],
    )

    class Meta:
        abstract = True

    def activate_language(self, request):
        # Do what LocaleMiddleware does.
        activate(self.language_code)
        request.LANGUAGE_CODE = get_language()
