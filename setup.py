import setuptools


def get_requirements(suffix=''):
    with open('requirements%s.txt' % suffix) as f:
        rv = f.read().splitlines()
    return rv


setuptools.setup(
    name="frink",
    version="0.0.3",
    url="https://github.com/hactar-is/frink",

    author="Hactar",
    author_email="systems@hactar.is",

    description="Basic ORM-like functionality for a RethinkDB datastore on top of Schematics.",
    long_description="""Basic ORM-like functionality for a RethinkDB datastore on top of
    Schematics. Includes datastores for use with Flask-Security.""",

    packages=setuptools.find_packages(),

    install_requires=get_requirements(),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
)
