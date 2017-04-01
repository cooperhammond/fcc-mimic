from setuptools import setup

setup(
    name =         'wire-mafia',
    version =      '0.0.1',
    description =  'Block select applications from the wifi. Like the mafia.',
    url =          'https://github.com/kepoorhampond/blockade',
    author =       'Kepoor Hampond',
    author_email = 'kepoorh@gmail.com',
    license =      'MIT',

    packages = ['wiremafia'],
    install_requires = [
      'draftlog',
    ],
    entry_points = {
      'console_scripts': ['mafia = wiremafia.cli:main'],
    },
)
