# -*- coding: utf-8 -*-

"""
TraceView API library

:copyright: (c) 2016 by Daniel Riti.
:license: MIT, see LICENSE for more details.

"""

__title__ = 'traceview'
__version__ = '0.7.0'
__author__ = 'Daniel Riti'
__license__ = 'MIT'


from .annotation import Annotation
from .api import Api
from .app import App, Assign
from .discovery import Action, Browser, Controller, Domain
from .discovery import Layer, Metric, Region
from .host import Host, Instrumentation
from .error import Rate
from .latency import Client, Server
from .organization import Organization
from .total_request import TotalRequests


class TraceView(object):
    """ The :class:`TraceView <TraceView>` object.

    Provides access to TraceView API resources.

    :param api_key: The TraceView API access key.
    :param func formatter: (optional) Function to format API results. See the module :mod:`traceview.formatters`.

    Usage::

      >>> import traceview
      >>> tv = traceview.TraceView('API KEY HERE')

    """

    def __init__(self, api_key, formatter=None):
        self._api = Api(api_key, after_request=formatter)

        self._actions = Action(self._api)
        self._annotation = Annotation(self._api)
        self._apps = App(self._api)
        self._assign = Assign(self._api)
        self._browsers = Browser(self._api)
        self._controllers = Controller(self._api)
        self._domains = Domain(self._api)
        self._error_rates = Rate(self._api)
        self._hosts = Host(self._api)
        self._instrumentation = Instrumentation(self._api)
        self._layers = Layer(self._api)
        self._metrics = Metric(self._api)
        self._organization = Organization(self._api)
        self._regions = Region(self._api)

        #: Get :py:class:`Client <traceview.latency.Client>` latency information.
        self.client = Client(self._api)
        #: Get :py:class:`Server <traceview.latency.Server>` latency information.
        self.server = Server(self._api)
        #: Get :py:class:`TotalRequests <traceview.total_request.TotalRequests>` information.
        self.total_requests = TotalRequests(self._api)


    def actions(self):
        """ Get all actions that have been traced.

        :return: all actions traced.
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.actions()
          [u'admin', u'products', u'blog', u'settings', u'logout']

        """
        return self._actions.get()

    def annotation(self, message, *args, **kwargs):
        """ Create an annotation.

        Annotations are used to log arbitrary events into TraceView, which are
        used to understand the correlation between system events (i.e. code
        release, server restarts, etc) and performance trends.

        :param str message: The annotation message.
        :param str appname: (optional) The application to associate the annotation with.
        :param str hostname: (optional) The host to associate the annotation with.
        :param str username: (optional) The user name to associate the annotation with.
        :param str layer: (optional) The layer name to associate the annotation with.
        :param str time: (optional) The time to associate the annotation with, in seconds since the epoch.

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.annotation('Code deployed', appname='production_web')

        """
        self._annotation.create(message, *args, **kwargs)

    def annotations(self, appname=None, *args, **kwargs):
        """ Get annotations.

        Annotations are used to log arbitrary events into TraceView, which are
        used to understand the correlation between system events (i.e. code
        release, server restarts, etc) and performance trends.

        The default time window is one week.

        :param str appname: (optional) The application name to filter annotations by.
        :param str time_start: (optional) The start time for the time window, in milliseconds since the epoch.
        :param str time_end: (optional) The end time for the time window, in milliseconds since the epoch.
        :rtype: list

        Usage::

          >>> import pprint
          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> pprint.pprint(tv.annotations(appname='production_web'))
          [{u'app': 3,
            u'host': u'prod-web.example.com',
            u'id': 123,
            u'message': u'Code deployed',
            u'time': 1409685758,
            u'username': u'dan'},
            ...
          ]

        """
        return self._annotation.get(app=appname, *args, **kwargs)

    def apps(self):
        """ Get all available applications.

        :return: all available applications
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.apps()
          [u'Default', u'flask_app']

        """
        return self._apps.get()

    def assign(self, hostname, appname, *args, **kwargs):
        """ Assign a host to an existing application.

        Please note that you cannot join host names to the `Default`
        application, as all hosts start there.

        :param str hostname: The host name to assign to the application.
        :param str appname: The existing application name.
        :param str layer: (optional) The layer name to assign to the application.

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.assign(hostname='web-app-1234', appname='production_web')

        """
        self._assign.update(hostname, appname, *args, **kwargs)

    def browsers(self):
        """ Get all browsers used by end users.

        :return: all browsers used by end users
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.browsers()
          [u'Chrome', u'Firefox', u'Links', u'Safari', u'Wii']

        """
        return self._browsers.get()

    def controllers(self):
        """ Get all controllers that have been traced.

        :return: all controllers traced
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.controllers()
          [u'admin', u'products', u'blog', u'settings', u'logout']

        """
        return self._controllers.get()

    def delete(self, host_id, *args, **kwargs):
        """
        .. deprecated:: 0.6.0
            Use :func:`delete_host <traceview.TraceView.delete_host>` instead.

        Delete an existing host.

        :param str host_id: The id of the host to delete.
        :return: indicates if host was successfully deleted.
        :rtype: boolean

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.delete(host_id='123')
          True

        """
        return self.delete_host(host_id, *args, **kwargs)

    def delete_host(self, host_id, *args, **kwargs):
        """ Delete an existing host.

        :param int host_id: The id of the host to delete.
        :return: indicates if host was successfully deleted.
        :rtype: boolean

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.delete_host(host_id=123)
          True

        """
        return self._hosts.delete(host_id, *args, **kwargs)

    def delete_app(self, app_name, *args, **kwargs):
        """ Delete an existing app.

        :param str app_name: The name of the app to delete.
        :return: indicates if app was successfully deleted.
        :rtype: boolean

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.delete_app(app_name='APP_123')
          True

        """
        return self._apps.delete(app_name, *args, **kwargs)

    def domains(self):
        """ Get all domains that have been traced.

        :return: all domains traced
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.domains()
          [u'example.com', u'www.example.com', u'mail.example.com']

        """
        return self._domains.get()

    def error_rates(self, app, *args, **kwargs):
        """ Get the error rate for an application.

        Each item in the items list is a pair of values (timestamp, error_rate).
        The error rate describes the number of traces with one or more errors,
        per total number of traces.

        :param str app: The application name.
        :return: timeseries data of the application's error rate
        :rtype: dict

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.error_rates('Default')
          {u'fields': u'timestamp,error_rate', u'items': [[1399082880.0, 0], [1399082910.0, 0], ...]}

        """
        return self._error_rates.get(app, *args, **kwargs)

    def hosts(self, appname=None, *args, **kwargs):
        """ Get all hosts that have been traced.

        :param str appname: (optional) The application name to filter hosts by.
        :return: all hosts traced
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.hosts()
          [{u'last_trace': None, u'last_heartbeat': 1429033545, u'first_heartbeat': 1428060977, u'name': u'ip-127-0-0-1', u'id': 12345}, { ... }]
        """
        return self._hosts.get(app=appname)

    def instrumentation(self, host_id):
        """ Get instrumentation version information for a host.

        :param str host_id: The id of the host.
        :return: instrumentation version information for a host
        :rtype: list

        Usage::

          >>> import pprint
          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> pprint.pprint(tv.instrumentation(host_id=1))
          [{u'name': u'tracelyzer',
            u'release_date': 1374537600,
            u'update_required': True,
            u'version': u'1.1.1'},
            ...
          ]

        """
        return self._instrumentation.get(host_id)

    def layers(self, app, *args, **kwargs):
        """ Get all recent layers for an application.

        The default time window for reported layers is 1 day.

        :param str app: The app name to list layers.
        :param int since_time: (optional) The start of the time window as a UTC timestamp in milliseconds.
        :return: all available apps
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.layers('Default')
          [u'PHP', u'cURL', u'lighttpd', u'php_mysql', u'php_mysqli']

        """
        return self._layers.get(app, *args, **kwargs)

    def licenses(self):
        """ Get the current number of hosts reporting traces and the number of
        hosts licensed to the organization.

        :return: licensing information for organization.
        :rtype: dict

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.licenses()
          {u'hosts_used': 5, u'hosts_limit': 10}

        """
        return self._organization.licenses()

    def metrics(self):
        """ Get all available host metrics that have been collected.

        :return: all avaiable host metrics being collected.
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.metrics()
          [u'cpu_user_frac:all', u'load', u'mem_apps', u'mem_cached', u'mem_swap', u'mem_totalused', ... ]

        """
        return self._metrics.get()

    def organization(self):
        """ Get organization information.

        :return: organization information
        :rtype: dict

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.organization()
          {u'fullname': u'the example organization', u'name': u'example'}

        """
        return self._organization.get()

    def regions(self):
        """ Get all geographical region codes of end users.

        Regions codes are ISO 3166-1 and ISO 3166-2 codes for all regions collected
        in RUM. Currently, country codes (ISO-3166-1) are available worldwide, and
        state codes (ISO-3166-2) are available in the US and Canada.

        :return: all geographical region codes of end users
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.regions()
          [u'CA', u'CA-BC', u'MX', u'RU', u'US', u'US-RI', ...]

        """
        return self._regions.get()

    def users(self):
        """ Get user information.

        :return: user information
        :rtype: list

        Usage::

          >>> import traceview
          >>> tv = traceview.TraceView('API KEY HERE')
          >>> tv.users()
          [{u'admin': True, u'name': u'Jane Doe', u'email': u'jdoe@example.com'}, { ... }]

        """
        return self._organization.users()
