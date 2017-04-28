#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import os

import cherrypy
import jinja2


class TemplateEngine:
    def __init__(self):
        self.args = {}

    def set(self, name: str, value):
        self.args.update({name: str(value)})

    def render_template(self, template_name: str) -> str:
        return ''


class Jinja2TemplateEngine(TemplateEngine):
    def __init__(self, templates_dir: str):
        super(Jinja2TemplateEngine, self).__init__()
        self.tmpl_loader = jinja2.FileSystemLoader(templates_dir, followlinks=True)
        #
        # print(self.tmpl_loader.list_templates())
        #
        self.env = jinja2.Environment(
            loader=self.tmpl_loader,
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )

    def render_template(self, template_name: str):
        if not template_name.endswith('.html'):
            template_name += '.html'
        template = self.env.get_template(template_name)
        return template.render(**self.args)


class HelloWorld:

    def __init__(self):
        self.te = Jinja2TemplateEngine('./tmpl')
        self.te.set('skin', 'default')

    @cherrypy.expose
    def index(self):
        return self.te.render_template('index')


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 80,
    })
    app_conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }
    cherrypy.quickstart(HelloWorld(), '/', app_conf)
