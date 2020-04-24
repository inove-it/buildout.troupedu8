# encoding: utf-8
from Products.CMFPlone.interfaces import constrains
from plone import api
from plone.app.contenttypes.migration.dxmigration import ContentMigrator
from plone.app.contenttypes.migration.migration import migrate as pac_migrate
from z3c.relationfield import RelationValue
from z3c.relationfield.event import updateRelations
from zope import component
from zope.intid.interfaces import IIntIds


class FolderGalerieMigrator(ContentMigrator):
    src_portal_type = 'Folder'
    src_meta_type = 'Dexterity Container'
    dst_portal_type = 'troupedu8.Galerie'
    dst_meta_type = None

    def migrate_schema_fields(self):
        for item in self.old.values():
            api.content.move(source=item, target=self.new)


class FolderGaleriePieceMigrator(ContentMigrator):
    src_portal_type = 'Folder'
    src_meta_type = 'Dexterity Container'
    dst_portal_type = 'troupedu8.GaleriePiece'
    dst_meta_type = None

    def migrate_schema_fields(self):
        intids = component.getUtility(IIntIds)
        piece = [i for i in api.content.find(portal_type='troupedu8.Piece') if i.Title == self.old.Title()][0]
        relpiece = RelationValue(intids.getId(piece.getObject()))
        self.new.piece = relpiece
        updateRelations(self.new, None)
        for item in self.old.values():
            api.content.move(source=item, target=self.new)


class GalerieGaleriePieceMigrator(FolderGaleriePieceMigrator):
    src_portal_type = 'troupedu8.Galerie'


def migrate(context):
    portal = api.portal.get()
    behavior = constrains.ISelectableConstrainTypes(api.content.get('/galerie'))
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(['troupedu8.Galerie', 'troupedu8.GaleriePiece'])
    behavior.setImmediatelyAddableTypes(['troupedu8.Galerie', 'troupedu8.GaleriePiece'])
    for galerie in api.content.get('/galerie').values():
        piece = [i for i in api.content.find(portal_type='troupedu8.Piece') if i.Title == galerie.Title()]
        if len(piece) == 1:
            pac_migrate(galerie, FolderGaleriePieceMigrator)
            pac_migrate(galerie, GalerieGaleriePieceMigrator)
        else:
            pac_migrate(galerie, FolderGalerieMigrator)
    brains = portal.portal_catalog(portal_type=['troupedu8.Galerie', 'troupedu8.GaleriePiece'])
    for brain in brains:
        collection = brain.getObject()
        collection.reindexObject()
