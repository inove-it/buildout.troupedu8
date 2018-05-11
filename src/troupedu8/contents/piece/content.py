# encoding: utf-8
from plone import api
from plone import schema
from plone.app.contenttypes.content import Event
from plone.app.contenttypes.interfaces import IEvent
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource
from plone.namedfile.field import NamedBlobImage
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.interface import implements


class RootCatalogSource(CatalogSource):

    def search_catalog(self, user_query):
        path = self.query.get('path')
        if path and path.get('query'):
            if not path.get('query').startswith('/'):
                path['query'] = '/'.join(api.content.get('/%s' % path.get('query')).getPhysicalPath())
        return super(RootCatalogSource, self).search_catalog(user_query)


class IPiece(IEvent):

    title = schema.TextLine(
        title=u"Titre",
        required=False,
    )

    auteur = schema.TextLine(
        title=u"Auteur",
        required=False,
    )

    description = schema.TextLine(
        title=u"Description",
        required=False,
    )

    text = RichText(
        title=u"Synopsis",
        required=False,
    )

    directeurs = RelationList(
        title=u"Metteur(s) en scène",
        value_type=RelationChoice(title=u"Directeur",
                                  source=RootCatalogSource(portal_type='troupedu8.Directeur', path={'query': 'metteurs-en-scene'}),
                                  ),
        required=True,
    )

    lieu = RelationChoice(
        title=u"Lieu",
        source=RootCatalogSource(portal_type='troupedu8.Lieu', path={'query': 'lieux'}),
        required=True,
    )

    image = NamedBlobImage(
        title=u"Photo de la pièce",
        required=False,
    )

    abonnement = schema.Bool(
        title=u"Spectacle dans l'abonnement",
        required=False,
    )

    dates = schema.List(
        title=u"Dates des représentations",
        value_type=schema.Datetime(),
        required=True,
    )

    facebook_url = schema.URI(
        title=u"Facebook",
        description=u"URL de l'évènement",
        required=False,
    )


class Piece(Event):
    implements(IPiece)

    @property
    def Heading(self):
        if self.auteur:
            return "%s <div class='autor'>de %s</div>" % (self.title, self.auteur)
        return self.title

    @property
    def start(self):
        self.dates.sort()
        return self.dates[0]

    @property
    def end(self):
        self.dates.sort()
        return self.dates[-1:][0]
