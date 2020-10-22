# encoding: utf-8
from plone.dexterity.browser.view import DefaultView


class ActeurView(DefaultView):

    def lf_to_p(self, text):
        if not text:
            return u"<p></p>"
        return u"<p>" + text.replace(u'\n', u'</p><p>') + u"</p>"
