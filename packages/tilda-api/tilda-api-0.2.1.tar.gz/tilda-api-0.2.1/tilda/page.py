# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 dotzero <mail@dotzero.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from tilda.base import TildaBase


class TildaPage(TildaBase):
    def __init__(self, *args, **kwargs):
        # Basic fields
        self.id = int(kwargs.get('id', 0))
        self.projectid = int(kwargs.get('projectid', 0))
        self.title = kwargs.get('title', '')
        self.descr = kwargs.get('descr', '')
        self.img = kwargs.get('img', '')
        self.featureimg = kwargs.get('featureimg', '')
        self.alias = kwargs.get('alias', '')
        self.date = self._fromdatestring(kwargs.get('date'))
        self.sort = int(kwargs.get('sort', 0))
        self.published = self._fromtimestamp(kwargs.get('published'))
        self.filename = kwargs.get('filename', '')
        self.html = kwargs.get('html', '')
        # Export fields
        self.css = kwargs.get('css', list())
        self.js = kwargs.get('js', list())
        self.images = kwargs.get('images', list())

    def __str__(self):
        return '(%d) %s' % (self.id, self.title)

    def __repr__(self):
        return '%s(%r)' % (self.__class__, self.__dict__)
