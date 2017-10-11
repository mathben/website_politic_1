#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import webbrowser
import tornado
import tornado.ioloop
import tornado.web
import tornado.httpserver
import handlers
from py_class import web_socket
from sockjs.tornado import SockJSRouter
import os
import subprocess
import base64

DEFAULT_SSL_DIRECTORY = os.path.join("..", "..", "ssl_cert")
CERT_FILE_SSL = os.path.join(DEFAULT_SSL_DIRECTORY, "ca.csr")
KEY_FILE_SSL = os.path.join(DEFAULT_SSL_DIRECTORY, "ca.key")


def main(parse_arg):
    socket_connection = SockJSRouter(web_socket.TestStatusConnection, '/update_user', user_settings=None)

    # TODO store cookie_secret if want to reuse it if restart server
    settings = {"static_path": parse_arg.static_dir,
                "template_path": parse_arg.template_dir,
                "debug": parse_arg.debug,
                "cookie_secret": base64.b64encode(os.urandom(50)).decode('ascii'),
                "login_url": "/login",
                "use_internet_static": parse_arg.use_internet_static,
                }
    routes = [
        # pages
        tornado.web.url(r"/", handlers.IndexHandler, name='index', kwargs=settings),
    ]
    application = tornado.web.Application(routes + socket_connection.urls, **settings)

    ssl_options = None
    if parse_arg.ssl:
        # use https if active ssl, secure http
        if not os.path.isfile(CERT_FILE_SSL) or not os.path.isfile(KEY_FILE_SSL):
            # Generate a self-signed certificate and key if we don't already have one.
            cmd = 'openssl req -x509 -sha256 -newkey rsa:2048 -keyout %s -out %s -days 36500 -nodes -subj' % (
                KEY_FILE_SSL, CERT_FILE_SSL)
            cmd_in = cmd.split() + ["/C=CA/ST=QC/L=Montreal/O=Politique/OU=politique.ca"]

            subprocess.call(cmd_in)

        ssl_options = {"certfile": CERT_FILE_SSL, "keyfile": KEY_FILE_SSL}

    io_loop = tornado.ioloop.IOLoop.instance()

    http_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_options, io_loop=io_loop)
    http_server.listen(port=parse_arg.listen.port)

    url = "http{2}://{0}:{1}".format(parse_arg.listen.address, parse_arg.listen.port, "s" if ssl_options else "")
    print('Starting server at {0}'.format(url))

    if parse_arg.open_browser:
        # open a URL, if possible on new tab
        webbrowser.open(url, new=2)

    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()
        io_loop.close()
