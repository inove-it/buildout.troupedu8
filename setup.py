# encoding: utf-8
from setuptools import find_packages
from setuptools import setup

setup(
    name='troupedu8',
    version='0.1',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
