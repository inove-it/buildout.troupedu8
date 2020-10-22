# encoding: utf-8
from plone import api
from plone import schema
from plone.dexterity.content import Item
from plone.dexterity.interfaces import IDexterityItem
from plone.namedfile.field import NamedBlobImage
from troupedu8.contents.piece.content import IPiece
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.interface import implements
from zope.intid.interfaces import IIntIds


class IActeur(IDexterityItem):

    firstname = schema.TextLine(
        title=u"Prénom",
        required=True,
    )
    lastname = schema.TextLine(
        title=u"Nom",
        required=False,
    )
    description = schema.Text(
        title=u"Description",
        required=False,
    )
    image = NamedBlobImage(
        title=u"Photo",
        required=False,
    )


class Acteur(Item):
    implements(IActeur)

    @property
    def title(self):
        first = self.firstname
        last = self.lastname
        return first + u" " + last if last else first

    @title.setter
    def title(self, value):
        pass

    @property
    def pieces(self):
        intids = getUtility(IIntIds)
        relation_catalog = getUtility(ICatalog)
        context_intid = intids.getId(self)
        relations = relation_catalog.findRelations({
            'to_id': context_intid,
            'from_interfaces_flattened': IPiece,
            'from_attribute': 'acteurs',
        })
        pieces = [r.from_object for r in relations if not r.isBroken()]
        return [a for a in pieces if api.content.get_state(obj=a) == 'published']
