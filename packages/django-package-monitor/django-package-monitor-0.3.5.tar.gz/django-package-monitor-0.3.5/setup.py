import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-package-monitor",
    version="0.3.5",
    packages=[
        'package_monitor',
        'package_monitor.management',
        'package_monitor.management.commands',
        'package_monitor.migrations',
    ],
    install_requires=[
        'requirements-parser>=0.1.0',
        'semantic_version>=2.5.0',
    ],
    include_package_data=True,
    description='Requirements package monitor for Django projects.',
    long_description=README,
    url='https://github.com/yunojuno/django-package-monitor',
    author='Hugo Rodger-Brown',
    author_email='hugo@yunojuno.com',
    maintainer='Hugo Rodger-Brown',
    maintainer_email='hugo@yunojuno.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
