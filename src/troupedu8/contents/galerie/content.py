# encoding: utf-8
from plone import api
from plone import schema
from plone.app.contenttypes.content import Folder
from plone.app.contenttypes.interfaces import IFolder
from plone.app.vocabularies.catalog import CatalogSource
from z3c.relationfield.schema import RelationChoice
from zope.interface import implements


class IGalerie(IFolder):

    title = schema.TextLine(
        title=u"Titre de la galerie",
        required=True,
    )

    start = schema.Date(
        title=u"Date",
        description=u"Utilisée pour filtrer sur la date de début/fin",
        required=False,
    )


class Galerie(Folder):
    implements(IGalerie)

    @property
    def end(self):
        return self.start


class RootCatalogSource(CatalogSource):

    def search_catalog(self, user_query):
        path = self.query.get('path')
        if path and path.get('query'):
            if not path.get('query').startswith('/'):
                path['query'] = '/'.join(api.content.get('/%s' % path.get('query')).getPhysicalPath())
        return super(RootCatalogSource, self).search_catalog(user_query)


class IGaleriePiece(IFolder):
    piece = RelationChoice(
        title=u"Pièce de la galerie",
        source=RootCatalogSource(portal_type='troupedu8.Piece', path={'query': 'pieces'}),
        required=True,
    )


class GaleriePiece(Folder):
    implements(IGaleriePiece)

    @property
    def title(self):
        return self.piece.to_object.Title()

    @title.setter
    def title(self, value):
        pass

    @property
    def start(self):
        self.piece.to_object.dates.sort()
        return self.piece.to_object.dates[0]

    @property
    def end(self):
        self.piece.to_object.dates.sort()
        return self.piece.to_object.dates[-1:][0]
