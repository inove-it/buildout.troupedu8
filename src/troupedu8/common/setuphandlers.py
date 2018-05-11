# encoding: utf-8
from plone import api
from Products.ATContentTypes.lib import constraintypes
from Products.CMFPlone.interfaces import constrains


def run_after(context):
    portal = api.portal.get()
    if not api.content.get('/slider-images'):
        slider = api.content.create(
            type='Folder',
            title='Slider images',
            id='slider-images',
            container=portal)
        slider.exclude_from_nav = True
        api.content.transition(slider, transition='publish')
    if not api.content.get('/metteurs-en-scene'):
        directors = api.content.create(
            type='Folder',
            title='Metteurs en scène',
            id='metteurs-en-scene',
            container=portal)
        api.group.grant_roles(
            groupname='AuthenticatedUsers',
            roles=['Contributor'],
            obj=directors)
        behavior = constrains.ISelectableConstrainTypes(directors)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        behavior.setLocallyAllowedTypes(['troupedu8.Directeur'])
        behavior.setImmediatelyAddableTypes(['troupedu8.Directeur'])
        api.content.transition(directors, transition='publish')
    if not api.content.get('/lieux'):
        lieux = api.content.create(
            type='Folder',
            title='Lieux',
            id='lieux',
            container=portal)
        api.group.grant_roles(
            groupname='AuthenticatedUsers',
            roles=['Contributor'],
            obj=lieux)
        behavior = constrains.ISelectableConstrainTypes(lieux)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        behavior.setLocallyAllowedTypes(['troupedu8.Lieu'])
        behavior.setImmediatelyAddableTypes(['troupedu8.Lieu'])
        lieux.exclude_from_nav = True
        api.content.transition(lieux, transition='publish')
    if not api.content.get('/pieces'):
        pieces = api.content.create(
            type='Folder',
            title='Agenda',
            id='pieces',
            container=portal)
        api.group.grant_roles(
            groupname='AuthenticatedUsers',
            roles=['Contributor'],
            obj=pieces)
        behavior = constrains.ISelectableConstrainTypes(pieces)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        behavior.setLocallyAllowedTypes(['troupedu8.Piece'])
        behavior.setImmediatelyAddableTypes(['troupedu8.Piece'])
        api.content.transition(pieces, transition='publish')
