#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
import re
from urllib import unquote

static_setting = {
    'templates': r'templates'
}


from HTTPerror import HTTP404Error, HTTP403Error, HTTP502Error


class RouteError(Exception):

    def __init__(self, info=None):
        print "<" + info + ">"

    def __str__(self):
        if(self.info == 'too many re'):
            return "<TOO MORE REGULAR SEARCH>"
        if(self.info == 'route error'):
            return '<WRONG ROUTE DESIGN>'
        if(self.info == 'query already in request'):
            return "<IT HAS ALREADY IN REQUEST VALUE>"


class RequestError(Exception):

    def __init__(self):
        pass


class RequestValueError(RequestError):

    def __str__(self):
        return "<the value has already in request's data>"


class WebApp():

    urls = []

    _parsed_urls = []

    global static_setting

    templates = False

    def __init__(self, environ=None, get_urls=True):
        self.request = {}

        if environ:
            self._environ = environ

            self._path = self._environ['PATH_INFO']
            if self._path[-1] != '/':
                self._path = self._path + '/'

            try:
                self.request['cookies'] = self._environ['HTTP_COOKIE']
            except KeyError:
                self.request['cookies'] = None

            self.request['http_protocol'] = self._environ['SERVER_PROTOCOL']

            self.request['user_agent'] = self._environ['HTTP_USER_AGENT']

            try:
                self.request['http_connect'] = self._environ['HTTP_CONNECTION']
            except KeyError:
                self.request['http_connect'] = None

            self.request['http_port'] = self._environ['HTTP_HOST']

            self.request['method'] = self._environ['REQUEST_METHOD']

            try:
                self.request['content_length'] = self._environ[
                    'CONTENT_LENGTH']
                self.request['content_type'] = self._environ['CONTENT_TYPE']
            except KeyError:
                self.request['content_length'] = None
                self.request['content_type'] = None

                self.request['http_accept_encoding'] = self._environ[
                    'HTTP_ACCEPT_ENCODING']

            self.request['data'] = {}
            self.request['query_string'] = {}

            line = self._environ['QUERY_STRING']
            request_data = environ['wsgi.input'].read()
            if request_data:
                request_data = unquote(request_data)
                for data_pair in request_data.split('&'):
                    key, value = data_pair.split('=')

                    self.request['data'][key] = value

            query_string = self._environ['QUERY_STRING']
            if query_string:
                query_string = unquote(query_string)
                for data_pair in query_string.split('&'):
                    try:
                        key, value = data_pair.split('=')
                        self.request['data'][key] = value
                        self.request['query_string'][key] = value
                    except ValueError:
                        pass

        if not get_urls:
            for url in self.urls:
                try:
                    res = self.url_parse(url[0])
                except RouteError:
                    print "<the route design got some mistakes>"
                    raise HTTP404Error

                if isinstance(res, tuple):
                    self._parsed_urls.append((res[0] + '$', url[1], res[1]))
                else:
                    self._parsed_urls.append((res + '$', url[1]))

        if self.templates:
            static_setting['templates'] = self.templates

    def __repr__(self):
        return "Jolla.WebAppObject"

    def __str__(self):
        return "<class 'Jolla.WebAppObject'>"

    def parse(self, urls):
        for url_handler in urls:
            if url_handler[0] == r'/':
                if self._path != '/':
                    continue
                else:
                    html_code = url_handler[1](self.request)

            url_reg = re.compile(url_handler[0])
            if url_reg.match(self._path):

                if '?' in url_handler[0]:
                    re_query = re.findall(url_reg, self._path)
                    if re_query[0]:

                        if url_handler[2] in self.request:
                            raise RouteError("query already in request")
                        else:

                            self.request[url_handler[2]] = re_query[0]
                            html_code = url_handler[1](self.request)
                            return html_code

                try:
                    html_code = url_handler[1](self.request)
                except TypeError:
                    html_code = url_handler[1]()

                return html_code
        raise HTTP404Error('REQUEST NOT FOUND IN ROUTE CONFIGURATION')

    def url_parse(self, path):

        path = path.replace(' ', '')
        if path[-1] != '/':
            path = path + '/'
        if '<' in path and '>' in path:
            if path.count("<") != path.count(">"):
                raise RouteError("route error")
            if path.count("<") > 1:
                raise RouteError("too many re")

            reg = re.compile(r'<(\w+)>')
            url_query = re.findall(reg, path)[0]
            the_url = path.replace('<' + url_query + '>',
                                   '(?P<' + url_query + '>\\w+)')
            return (the_url, url_query)
        return path

    def get_parsed_urls(self):
        return self._parsed_urls


class jolla_server(WSGIServer):

    def __init__(self, app, port=8000, host="127.0.0.1", debug=False):
        self.port = port
        self.host = host
        self.app = app

        my_app = self.app(get_urls=False)
        self.urls = my_app.get_parsed_urls()

        WSGIServer.__init__(self, listener=(
            self.host, self.port), application=self.application)

    def __str__(self):
        return "<class 'Jolla.jolla_serverObeject'>"

    def __repr__(self):
        return 'Jolla.jolla_serverObeject'

    def application(self, environ, start_response):

        try:
            the_app = self.app(environ)
            html_code = the_app.parse(self.urls)
            if not isinstance(html_code, tuple):
                html_code = (html_code, ('Content-Type', 'text/html'))
            status = '200 OK'
        except HTTP404Error:
            status = '404 NOT FOUND'
            html_code = ('404 NOT FOUND', ('Content-Type', 'text/html'))

        header = [
            ('Server', 'Jolla/1.0')
        ]

        for i in range(1, len(html_code)):
            header.append(html_code[i])

        start_response(status, header)

        return html_code[0]

    def run_server(self):
        print "the server is running on the {} in the port {}".format(self.host, self.port)

        self.serve_forever()
