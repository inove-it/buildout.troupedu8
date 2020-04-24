# encoding: utf-8
from datetime import datetime
from plone import api
from z3c.relationfield import RelationValue
from zope import component
from zope.intid.interfaces import IIntIds

import csv


def migrate(context):
    intids = component.getUtility(IIntIds)
    pieces = api.content.get('/pieces')

    with open('data.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            title = row['titre']
            auteur = row['auteur']
            abonnement = True if row['abonnement'] == '1' else False
            commentaire = row['commentaire']
            lieu = row['localite']
            directeurs = row['metteurenscene'].split(' & ')
            dates = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in row['date'].split(',')]
            for directeur in directeurs:
                dbdirecteur = [i for i in api.content.find(portal_type='troupedu8.Directeur') if i.Title == directeur]
                if not dbdirecteur:
                    splitdir = directeur.split(' ')
                    firstname = splitdir[0]
                    lastname = ''
                    if len(splitdir) > 1:
                        lastname = splitdir[1]
                    api.content.create(type='troupedu8.Directeur', title=directeur.decode('utf8'), firstname=firstname.decode('utf8'), lastname=lastname.decode('utf8'), container=api.content.get('/metteurs-en-scene'))
            dblieu = [i for i in api.content.find(portal_type='troupedu8.Lieu') if i.Title == lieu]
            if not dblieu:
                api.content.create(type='troupedu8.Lieu', title=lieu.decode('utf8'), container=api.content.get('/lieux'))

            rellieu = RelationValue(intids.getId([i for i in api.content.find(portal_type='troupedu8.Lieu') if i.Title == lieu][0].getObject()))
            reldirecteurs = []
            for directeur in directeurs:
                reldirecteurs.append(RelationValue(intids.getId([i for i in api.content.find(portal_type='troupedu8.Directeur') if i.Title == directeur][0].getObject())))

            dbpiece = [i for i in api.content.find(portal_type='troupedu8.Piece') if i.Title == title]
            if not dbpiece:
                newpiece = api.content.create(type='troupedu8.Piece',
                                              title=title.decode('utf8'),
                                              auteur=auteur.decode('utf8'),
                                              abonnement=abonnement,
                                              dates=dates,
                                              description=commentaire.decode('utf8'),
                                              directeurs=reldirecteurs,
                                              lieu=rellieu,
                                              container=pieces)
                api.content.transition(newpiece, transition='publish')
