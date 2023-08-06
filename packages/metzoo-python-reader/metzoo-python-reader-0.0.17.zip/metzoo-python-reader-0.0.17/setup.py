# -*- coding: utf-8 -*-

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

config = {
    'name': 'metzoo-python-reader',
    'version': '0.0.17',
    'description': 'Python Data Reader for Metzoo',
    'long_description': readme(),
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    'entry_points': {
        'console_scripts': [
            'metzoo-reader = metzoo.reader.reader:main'
        ]
    },
    'data_files': [
        ('metzoo-python-reader/config', ['config-template.yaml'])
    ],
    'keywords': 'metzoo monitoring metric',
    'url': 'https://bitbucket.org/edrans/metzoo-python-reader',
    'author': 'Edrans',
    'author_email': 'info@edrans.com',
    'license': 'MIT',
    'packages': ['metzoo', 'metzoo.reader'],
    'install_requires': ['pyaml', 'metzoo-python-lib'],
    'zip_safe': False
}

setup(**config)
