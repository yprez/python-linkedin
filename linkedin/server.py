# -*- coding: utf-8 -*-
from __future__ import print_function
import future.moves.http.server as http_server
import future.moves.urllib.parse as urllib_parse

from .linkedin import LinkedInApplication, LinkedInAuthentication, PERMISSIONS


def quick_api(api_key, secret_key, port=8000):
    """
    This method helps you get access to linkedin api quickly when using it
    from the interpreter.
    Notice that this method creates http server and wait for a request, so it
    shouldn't be used in real production code - it's just an helper for debugging

    The usage is basically:
    api = quick_api(KEY, SECRET)
    After you do that, it will print a URL to the screen which you must go in
    and allow the access, after you do that, the method will return with the api
    object.
    """
    auth = LinkedInAuthentication(api_key, secret_key, 'http://localhost:8000/',
                                  list(PERMISSIONS.enums.values()))
    app = LinkedInApplication(authentication=auth)
    print(auth.authorization_url)
    _wait_for_user_to_enter_browser(app, port)
    return app


def _wait_for_user_to_enter_browser(app, port):
    class MyHandler(http_server.BaseHTTPRequestHandler):
        def do_GET(self):
            p = self.path.split('?')
            if len(p) > 1:
                params = urllib_parse.parse_qs(p[1], True, True)
                app.authentication.authorization_code = params['code'][0]
                app.authentication.get_access_token()

    server_address = ('', port)
    httpd = http_server.HTTPServer(server_address, MyHandler)
    httpd.handle_request()
