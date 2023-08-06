# -*- coding: utf-8 -*-

"""
traceview.app

This module contains the objects associated with App Management API resources.

http://dev.appneta.com/docs/api-v2/app.html

"""

from .resource import Resource


class Assign(Resource):

    def update(self, hostname, app, *args, **kwargs):
        kwargs['hostname'] = hostname
        kwargs['appname'] = app
        return self.api.post('assign_app', *args, **kwargs)


class App(Resource):

    def get(self):
        return self.api.get('apps')

    def delete(self, app_name, *args, **kwargs):
        path = 'app/{app_name}'.format(app_name=app_name)
        return self.api.delete(path)
