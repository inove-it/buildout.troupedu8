# encoding: utf-8
from plone import schema
from plone.dexterity.content import Item
from plone.dexterity.interfaces import IDexterityItem
from plone.namedfile.field import NamedBlobImage
from zope.interface import implements


class ILieu(IDexterityItem):

    title = schema.TextLine(
        title=u"Titre du lieu",
        required=True,
    )
    description = schema.Text(
        title=u"Description",
        required=False,
    )
    image = NamedBlobImage(
        title=u"Photo du lieu",
        required=False,
    )


class Lieu(Item):
    implements(ILieu)
