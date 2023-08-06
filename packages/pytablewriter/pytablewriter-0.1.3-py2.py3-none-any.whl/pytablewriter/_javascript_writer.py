# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import re

import dataproperty
import six

from ._error import EmptyTableNameError
from ._text_writer import SourceCodeTableWriter


class JavaScriptTableWriter(SourceCodeTableWriter):
    """
    Concrete class of a table writer for JavaScript format.

    :Examples:

        :ref:`example-js-table-writer`
    """

    def __init__(self):
        super(JavaScriptTableWriter, self).__init__()

        self._prop_extractor.none_value = "null"
        self.__re_replace_null = re.compile('["]null["]', re.MULTILINE)

    def write_table(self):
        """
        |write_table| with JavaScript nested list variable definition format.
        """

        self._verify_property()
        self._preprocess()

        org_stream = self.stream
        self.stream = six.StringIO()

        self.inc_indent_level()
        super(JavaScriptTableWriter, self).write_table()
        self.dec_indent_level()
        data_frame_text = self.stream.getvalue().rstrip(u",\n")
        data_frame_text = self.__re_replace_null.sub(
            self._prop_extractor.none_value, data_frame_text)

        self.stream.close()
        self.stream = org_stream

        self._write_line(u"var %s = [" % (self.variable_name))
        self.dec_indent_level()
        self._write_line(data_frame_text)
        self.inc_indent_level()
        self._write_line(u"];")

    def _verify_table_name(self):
        if dataproperty.is_empty_string(self.table_name):
            raise EmptyTableNameError()
