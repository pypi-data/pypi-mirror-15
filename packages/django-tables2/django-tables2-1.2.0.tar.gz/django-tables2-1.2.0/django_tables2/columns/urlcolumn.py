# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.db import models

from .base import library
from .linkcolumn import BaseLinkColumn


@library.register
class URLColumn(BaseLinkColumn):
    """
    Renders URL values as hyperlinks.

    :param text: Either static text, or a callable. If set, this
                 value will be used to render the text inside link
                 instead of value (default)
    :param attrs: Additional attributes for the ``<a>`` tag

    Example::

        >>> class CompaniesTable(tables.Table):
        ...     www = tables.URLColumn()
        ...
        >>> table = CompaniesTable([{'www': 'http://google.com'}])
        >>> table.rows[0].get_cell('www')
        u'<a href="http://google.com">http://google.com</a>'

    """
    def render(self, record, value):
        return self.render_link(value, record=record, value=value)

    @classmethod
    def from_field(cls, field):
        if isinstance(field, models.URLField):
            return cls(verbose_name=field.verbose_name)
