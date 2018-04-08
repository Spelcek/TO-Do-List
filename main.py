#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Sporocilo

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))



class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("pozdrav.html")


class ToDoVnosHandler(BaseHandler):
    def post(self):
        params = {}
        opravilo = self.request.get("opravilo")
        avtor = self.request.get("avtor")

        seznam = Sporocilo(opravilo=opravilo, avtor=avtor)
        seznam.put()

        self.redirect("/ToDoBaza")

    def get(self):
        return self.render_template("ToDoVnos.html")


class SeznamVnosovHandler(BaseHandler):
    def get(self):
        seznam = Sporocilo.query().fetch()
        params = {"seznam": seznam}
        return self.render_template("ToDoBaza.html", params=params)

class UrediVnosHandler(BaseHandler):
    def get(self, seznam_id):
        seznam = Sporocilo.get_by_id(int(seznam_id))

        params = {"seznam": seznam}

        return self.render_template("uredi-seznam.html", params=params)
    def post(self, seznam_id):
        o1 = self.request.get("opravilo")
        a1 = self.request.get("avtor")


        seznam = Sporocilo.get_by_id(int(seznam_id))
        seznam.opravilo = o1
        seznam.avtor = a1
        seznam.put()

        params = {"seznam": seznam}

        return self.render_template("uredi-seznam.html", params=params)

class IzbrisiVnosHandler(BaseHandler):
    def get(self, seznam_id):
        seznam = Sporocilo.get_by_id(int(seznam_id))

        params = {"seznam": seznam}

        return self.render_template("Izbrisi-ToDoVnos.html", params=params)

    def post(self, seznam_id):

        seznam = Sporocilo.get_by_id(int(seznam_id))
        seznam.key.delete()

        return self.redirect_to("seznam-tukaj")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/ToDoVnos', ToDoVnosHandler),
    webapp2.Route('/ToDoBaza', SeznamVnosovHandler, name="seznam-tukaj"),
    webapp2.Route('/uredi-seznam/<seznam_id:\d+>', UrediVnosHandler),
    webapp2.Route('/Izbrisi-ToDoVnos/<seznam_id:\d+>', IzbrisiVnosHandler),
], debug=True)



