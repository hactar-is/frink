import setuptools

setuptools.setup(
    name="frink",
    version="0.0.1",
    url="https://github.com/hactar-is/frink",

    author="Hactar",
    author_email="systems@hactar.is",

    description="Basic ORM-like functionality for a RethinkDB datastore on top of Schematics.",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=['schematics', 'rethinkdb', 'flask-security'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
)
