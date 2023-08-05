# -*- coding: utf-8 -*-

# Copyright 2010 Dirk Holtwick, holtwick.it
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import xhtml2pdf.pisa as pisa
from six import StringIO

import logging


log = logging.getLogger("xhtml2pdf.wsgi")


class Filter(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('SCRIPT_NAME', '')
        path_info = environ.get('PATH_INFO', '')
        sent = []
        written_response = StringIO.StringIO()

        def replacement_start_response(status, headers, exc_info=None):
            if not self.should_filter(status, headers):
                return start_response(status, headers, exc_info)
            else:
                sent[:] = [status, headers, exc_info]
                return written_response.write

        app_iter = self.app(environ, replacement_start_response)
        if not sent:
            return app_iter
        status, headers, exc_info = sent
        try:
            for chunk in app_iter:
                written_response.write(chunk)
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()
        body = written_response.getvalue()
        status, headers, body = self.filter(
            script_name, path_info, environ, status, headers, body)
        start_response(status, headers, exc_info)
        return [body]

    def should_filter(self, status, headers):
        print (headers)

    def filter(self, status, headers, body):
        raise NotImplementedError


class HTMLFilter(Filter):
    def should_filter(self, status, headers):
        if not status.startswith('200'):
            return False
        for name, value in headers:
            if name.lower() == 'content-type':
                return value.startswith('text/html')
        return False


class PisaMiddleware(HTMLFilter):
    def filter(self, script_name, path_info, environ, status, headers, body):
        topdf = environ.get("pisa.topdf", "")
        if topdf:
            dst = StringIO.StringIO()
            pisa.CreatePDF(body, dst, show_error_as_pdf=True)
            headers = [
                ("content-type", "application/pdf"),
                ("content-disposition", "attachment; filename=" + topdf)
            ]
            body = dst.getvalue()
        return status, headers, body
