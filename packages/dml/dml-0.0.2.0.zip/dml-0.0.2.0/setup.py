from distutils.core import setup

setup(
    name             = 'dml',
    version          = '0.0.2.0',
    packages         = ['dml',],
    install_requires = ['pymongo','json',],
    license          = 'MIT License',
	url              = 'http://datamechanics.org',
	author           = 'A. Lapets',
	author_email     = 'a@lapets.io',
    description      = 'Common functionalities for building Data Mechanics platform components.',
    long_description = open('README').read(),
)
