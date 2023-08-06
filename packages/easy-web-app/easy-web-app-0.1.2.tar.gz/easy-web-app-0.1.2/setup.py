import os
from setuptools import setup, find_packages

def read( fname ):
    return open( os.path.join( os.path.dirname(__file__), fname ) ).read()

setup(
    name='easy-web-app',
    version = "0.1.2",
    packages = ["easywebapp"],
    #scripts = ['webapp.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['web.py','nose','WebTest'],

    #package_data = {
    #    # If any package contains *.txt or *.rst files, include them:
    #    '': ['*.txt', '*.rst'],
    #    # And include any *.msg files found in the 'hello' package, too:
    #    'hello': ['*.msg'],
    #},

    # metadata for upload to PyPI
    author = "ma-ha",
    author_email = "ma@mh-svr.de",
    description='Create web applications easily by defining them in JSON format.',
    keywords = "GUI web app browser AJAX easy portal REST RESTful web service form table I/O content serverless API centric",
    url = "https://github.com/ma-ha/easy-py-web-app",
    license='MIT',
    long_description=read('README.rst'),
    test_suite = 'nose.collector',
         
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)