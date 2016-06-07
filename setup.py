import ast
import setuptools

with open('frink/__init__.py') as f:
    for line in f:
        if line.startswith('__version__'):
            version = ast.parse(line).body[0].value.s
            break

assert version is not None

setuptools.setup(
    name="frink",
    version=version,

    url="https://github.com/hactar-is/frink",

    author="Hactar",
    author_email="systems@hactar.is",

    description="Basic ORM-like functionality for a RethinkDB datastore on top of Schematics.",
    long_description="""Basic ORM-like functionality for a RethinkDB datastore on top of
    Schematics. Includes datastores for use with Flask-Security.""",

    packages=setuptools.find_packages(),

    install_requires=[
        'schematics',
        'rethinkdb==2.3.0',
        'inflection',
        'future'
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
)
