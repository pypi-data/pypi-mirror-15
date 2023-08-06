import json
import logging
import re
from collections import Iterable

import bleach
import markdown
from django.core.urlresolvers import reverse, get_resolver, RegexURLResolver, RegexURLPattern, NoReverseMatch
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.test import Client
from django.test import TestCase
from django.utils.timezone import now
from django.views.static import serve

from shark import models
from shark.actions import JS, JQ, BaseAction, URL
from shark.common import listify
from shark.models import EditableText, StaticPage as StaticPageModel
from shark.objects.analytics import GoogleAnalyticsTracking
from shark.objects.layout import Div, Spacer, Row
from shark.objects.navigation import NavLink
from shark.settings import SharkSettings
from .base import Collection, BaseObject, PlaceholderWebObject, Default, ALLOWED_TAGS, ALLOWED_ATTRIBUTES, \
    ALLOWED_STYLES, Markdown, Renderer
from .resources import Resources

unique_name_counter = 0

class BaseHandler:
    route = None
    redirects = None

    def __init__(self, *args, **kwargs):
        pass

    def render(self, request):
        raise Http404("Not Implemented")

    unique_name = None
    @classmethod
    def get_unique_name(cls):
        if not cls.unique_name:
            global unique_name_counter
            unique_name_counter += 1
            cls.unique_name = '{}-{}'.format(cls.__name__, unique_name_counter)

        return cls.unique_name

    @classmethod
    def url(cls, *args, **kwargs):
        return URL(reverse('shark:' + cls.get_unique_name(), args=args, kwargs=kwargs, current_app='shark'), False)

    @classmethod
    def sitemap(cls):
        return True

    @classmethod
    def get_sitemap(cls, include_false=False):
        sitemap = cls.sitemap()
        if sitemap == True or (sitemap == False and include_false):
            try:
                u = cls.url()
                return [[]]
            except NoReverseMatch:
                return []
        elif isinstance(sitemap, str):
            return [sitemap]
        elif isinstance(sitemap, list):
            return sitemap

        return []


class NotFound404(Exception):
    pass


class BasePageHandler(BaseHandler):
    ignored_variables = ['items', 'modals', 'nav', 'container', 'base_object', 'current_user', 'user']

    def __init__(self, *args, **kwargs):
        self.title = ''
        self.description = ''
        self.keywords = ''
        self.author = ''
        self.robots_index = True
        self.robots_follow = True

        self.items = Collection()
        self.base_object = self.items
        self.modals = Collection()
        self.nav = None
        self.crumbs = []
        self.main = None
        self.footer = None

        self.javascript = ''

        self.resources = Resources()
        self.resources.add_resource('http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css', 'css', 'bootstrap', 'main')

        print('Handler created', now())

    def init(self):
        pass

    def output_html(self, args, kwargs):
        print('Start output HTML', now())
        content = Collection()
        content.append(self.modals)
        content.append(self.nav)
        content.append(self.main)
        if self.crumbs:
            self.base_object.insert(0, Spacer())
            self.base_object.insert(1, Row(Div(BreadCrumbs(*self.crumbs), classes='col-md-12')))
        content.append(self.items)
        content.append(self.footer)

        keep_variables = {}
        for variable_name in dir(self):
            if variable_name not in self.ignored_variables:
                variable = self.__getattribute__(variable_name)
                if isinstance(variable, BaseObject):
                    variable.id_needed()
                    keep_variables[variable_name] = variable.serialize()

        renderer = Renderer(self)
        print('Start render', now())
        renderer.render('        ', content)
        print('End render', now(), renderer.render_count)

        html = render(self.request, 'base.html', {
                                  'title': self.title,
                                  'description': self.description.replace('"', '\''),
                                  'keywords': self.keywords,
                                  'author': self.author,
                                  'content': renderer.html,
                                  'extra_css': '\r\n'.join(['        <link rel="stylesheet" href="' + css_resource.url + '" id="resource-{}-{}"/>'.format(css_resource.module, css_resource.name) for css_resource in renderer.css_resources]),
                                  'extra_js': '\r\n'.join(['        <script src="' + js_file + '"></script>' for js_file in renderer.js_files]),
                                  'javascript': renderer.js,
                                  'css': renderer.css,
                                  'keep_variables': keep_variables
        })

        print('End output HTML', now())
        return html


    def render(self, request, *args, **kwargs):
        self.request = request
        self.user = self.request.user

        if request.method == 'GET':
            self.init()
            if SharkSettings.SHARK_GOOGLE_ANALYTICS_CODE:
                self.append(GoogleAnalyticsTracking(SharkSettings.SHARK_GOOGLE_ANALYTICS_CODE))
            try:
                self.render_page(*args, **kwargs)
            except NotFound404:
                raise Http404()
            else:
                output = self.output_html(args, kwargs)
            return output
        elif request.method == 'POST':
            action = self.request.POST.get('action', '')
            keep_variables = json.loads(self.request.POST.get('keep_variables', '{}'))
            keep_variable_objects = []
            for variable_name in keep_variables:
                placeholder = PlaceholderWebObject(
                    self,
                    keep_variables[variable_name]['id'],
                    keep_variables[variable_name]['class_name']
                )
                keep_variable_objects.append(placeholder)

                self.__setattr__(variable_name, placeholder)

            arguments = {}
            for argument in self.request.POST:
                if argument not in ['action', 'keep_variables', 'csrfmiddlewaretoken']:
                    arguments[argument] = self.request.POST[argument]

            self.renderer = Renderer()

            if action:
                self.__getattribute__(action)(*args, **arguments)

            javascript = [self.javascript]

            for obj in keep_variable_objects:
                self.renderer.render_variables(obj.variables)

            javascript.append(self.renderer.js)

            for obj in keep_variable_objects:
                javascript.extend([jq.js for jq in obj.jqs])

            data = {'javascript': ''.join(javascript),
                    'html': '',
                    'data': ''}
            json_data = json.dumps(data)

            return HttpResponse(json_data)

    def append(self, *items):
        self.base_object.append(*items)
        if items:
            return items[0]
        else:
            return None

    def append_row(self, *args, **kwargs):
        self.append(Row(Div(args, classes='col-md-12'), **kwargs))

    def add_javascript(self, script):
        if isinstance(script, BaseAction):
            self.javascript += script.js
        elif isinstance(script, JQ):
            self.javascript += script.js
        else:
            self.javascript = self.javascript + script

    def render_page(self):
        raise NotImplementedError

    def text(self, name, default_txt=None):
        text = EditableText.load(name)
        if not text:
            text = EditableText()
            text.name = name
            text.content = default_txt or name
            text.filename = ''
            text.handler_name = self.__class__.__name__
            text.line_nr = 0
            text.last_used = now()
            text.save()

        return text.content

    def replace_resource_js(self, resource):
        return JS('$("#resource-{}-{}").attr("href", "{}").on("load", function(){{$(window).resize()}});'.format(resource.module, resource.name, resource.url))

    # def _handle_form_post(self, *args, post_action='', form_data='', **kwargs):
    #     form_data = {item.split('=', 1)[0]: item.split('=', 1)[1] for item in signing.loads(form_data).split('|')}
    #     form_id = form_data['formid']
    #     form_class_description = form_data['form']
    #     form_class_name = re.match('(.*)\((.*)\)', form_class_description).group(1)
    #     form_class_params = re.match('(.*)\((.*)\)', form_class_description).group(2)
    #     form_error_class = form_data['formerror']
    #
    #     form = SharkForm.sub_classes[form_class_name]()
    #     form.deserialize(form_class_params)
    #     formerror = FormError.sub_classes[form_error_class](form_id)
    #     form.setup_post(kwargs)
    #
    #     form._validate()
    #     if not form.errors:
    #         if post_action:
    #             self.__getattribute__(post_action)(*args, form)
    #         else:
    #             form.save()
    #     else:
    #         renderer = Renderer()
    #         for error in form.errors:
    #             error_object = formerror
    #             if error.field and ('fld-' + error.field.full_name) in form_data:
    #                 error_object = FieldError.sub_classes[form_data['fld-' + error.field.full_name]](error.field.full_name)
    #
    #             if error_object:
    #                 selector = "$('#{} .{}')".format(form_id, error_object.html_class_name)
    #                 error_renderer = Renderer()
    #                 error_object._render_error(error_renderer, error.message)
    #                 self.javascript += JQ(selector, renderer=renderer).append_raw(error_renderer.html).js
    #                 self.javascript += error_renderer.js
    #             print(error.field, error.message)
    #
    #         renderer.render('', None)
    #         self.javascript = renderer.js + self.javascript


def exists_or_404(value):
    if not value:
        raise Http404()
    return value


class HandlerTestCase(TestCase):
    def setUp(self):
        pass

    url = None
    def test_response_is_200(self):
        if self.__class__.url:
            logging.info('URL', self.__class__.url)
            client = Client()
            response = client.get(self.__class__.url)

            self.assertEqual(response.status_code, 200)


class Container(BaseObject):
    def __init__(self, items=Default, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Items in the container', Collection())
        self.add_class('container')

    def get_html(self, html):
        html.append('<div' + self.base_attributes + '>')
        html.render('    ', self.items)
        html.append('</div>')

    def insert(self, i, x):
        self.items.insert(i, x)


class BaseContainerPageHandler(BasePageHandler):
    def __init__(self, *args, **kwargs):
        super(BaseContainerPageHandler, self).__init__(*args, **kwargs)

        self.container = Container()
        self.items.append(self.container)
        self.base_object = self.container


def shark_django_handler(request, *args, handler=None, **kwargs):
    handler_instance = handler()
    outcome = handler_instance.render(request, *args, **kwargs)
    return outcome


def shark_django_redirect_handler(request, *args, handler=None, function=None, **kwargs):
    if function:
        if isinstance(function, str):
            url = handler().__getattribute__(function)(request, *args, **kwargs)
        else:
            url = handler.url(*listify(function(request, *args, **kwargs)))
    else:
        url = handler.url(*args, **kwargs)

    return HttpResponsePermanentRedirect(url)


class StaticPage(BasePageHandler):
    def render_page(self, url_name):
        page = StaticPageModel.load(url_name)
        if not page:
            raise NotFound404()

        self.title = page.title
        self.description = page.description
        self.append(Markdown(page.body))

        if self.user.is_staff and self.user.has_perm('shark.staticpage_change'):
            if self.nav:
                self.nav.right_items.append(NavLink('Edit Page', reverse('admin:shark_staticpage_change', args=[page.url_name])))

    @classmethod
    def url(cls, *args, **kwargs):
        return URL(reverse('shark:shark_static_page', args=args, kwargs=kwargs), False)

    @classmethod
    def sitemap(cls):
        pages = models.StaticPage.objects.filter(sitemap=True).all()
        return [sp.url_name for sp in pages]


def markdown_preview(request):
    """ Render preview page.
    :returns: A rendered preview
    """
    user = getattr(request, 'user', None)
    if not user or not user.is_staff:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())

    dirty = markdown.markdown(text=escape(request.POST.get('data', 'No content posted')), output_format='html5')
    value = bleach.clean(dirty, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
    return HttpResponse(value)


class Robots(BaseHandler):
    route = '^robots.txt$'

    def render(self, request):
        return HttpResponse(
            "User-agent: *\r\n" +
            "Disallow: /admin/*\r\n" +
            "Disallow: /__debug__/*"
        )

    @classmethod
    def sitemap(cls):
        return False


class SiteMap(BaseHandler):
    route = '^sitemap.xml$'

    def get_urls(self, include_false=False):
        urls = set()

        handlers = set()

        def add_patterns(patterns):
            for pattern in patterns:
                if isinstance(pattern, RegexURLResolver):
                    add_patterns(pattern.url_patterns)
                elif isinstance(pattern, RegexURLPattern):
                    if 'handler' in pattern.default_args and issubclass(pattern.default_args['handler'], BaseHandler):
                        handler = pattern.default_args['handler']
                        if handler not in handlers:
                            handlers.add(handler)
                            for args in handler.get_sitemap(include_false):
                                if isinstance(args, str) or not isinstance(args, Iterable):
                                    args=[args]
                                urls.add(handler.url(*args))

        add_patterns(get_resolver().url_patterns)

        return urls

    def render(self, request):
        lines = []
        lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        handlers = set()
        for url in self.get_urls():
            lines.append('    <url><loc>{}</loc></url>'.format(request.build_absolute_uri(url.url)))

        lines.append('</urlset>')
        return HttpResponse('\r\n'.join(lines))

    @classmethod
    def sitemap(cls):
        return False


class Favicon(BaseHandler):
    route = '^favicon.ico$'

    def render(self, request):
        return serve(request, 'favicon.ico', 'static/icons')


class GoogleVerification(BaseHandler):
    def render(self, request):
        return HttpResponse('google-site-verification: {}.html'.format(SharkSettings.SHARK_GOOGLE_VERIFICATION))

    @classmethod
    def sitemap(cls):
        return False


class BingVerification(BaseHandler):
    def render(self, request):
        return HttpResponse('<?xml version="1.0"?><users><user>{}</user></users>'.format(SharkSettings.SHARK_BING_VERIFICATION))

    @classmethod
    def sitemap(cls):
        return False


class YandexVerification(BaseHandler):
    def render(self, request):
        return HttpResponse('<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body>Verification: {}</body></html>'.format(SharkSettings.SHARK_YANDEX_VERIFICATION))

    @classmethod
    def sitemap(cls):
        return False