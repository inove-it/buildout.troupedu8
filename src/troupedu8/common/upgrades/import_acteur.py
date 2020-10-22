# encoding: utf-8
from plone import api
from z3c.relationfield import RelationValue
from zope import component
from zope.intid.interfaces import IIntIds
from z3c.relationfield.event import updateRelations

import csv


def migrate(context):
    intids = component.getUtility(IIntIds)
    portal = api.portal.get()

    with open('acteurs.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter='|')
        for row in csv_reader:
            piece = row['piece']
            acteur = row['acteur']
            prenom = acteur.split(' ')[0]
            nom = ' '.join(acteur.split(' ')[1:])
            dbpiece = [i for i in api.content.find(portal_type='troupedu8.Piece') if i.Title == piece]
            dbacteur = [i for i in api.content.find(portal_type='troupedu8.Acteur') if i.Title == acteur]
            if not dbpiece:
                raise Exception("%s n'existe pas" % piece)
            elif len(dbpiece) > 1:
                raise Exception("%s existe plusieurs fois" % piece)
            else:
                dbpiece = dbpiece[0].getObject()
            if not dbacteur:
                dbacteur = api.content.create(type='troupedu8.Acteur', title=acteur.decode('utf8'), firstname=prenom.decode('utf8'), lastname=nom.decode('utf8'), container=api.content.get('/acteurs'))
                api.content.transition(dbacteur, transition='publish')
            elif len(dbacteur) > 1:
                raise Exception("%s existe plusieurs fois" % acteur)
            else:
                dbacteur = dbacteur[0].getObject()
            if not dbpiece.acteurs:
                dbpiece.acteurs = [RelationValue(intids.getId(dbacteur))]
            else:
                if intids.getId(dbacteur) not in [i.to_id for i in dbpiece.acteurs]:
                    dbpiece.acteurs.append(RelationValue(intids.getId(dbacteur)))
            updateRelations(dbpiece, None)
            updateRelations(dbacteur, None)
            dbpiece.reindexObject()

    brains = portal.portal_catalog(portal_type=['troupedu8.Acteur', 'troupedu8.Piece'])
    for brain in brains:
        collection = brain.getObject()
        updateRelations(collection, None)
        collection.reindexObject()
