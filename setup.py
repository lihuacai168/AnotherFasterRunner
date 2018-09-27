#encoding: utf-8
import io
import os


from setuptools import find_packages, setup

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'FasterRunner', '__about__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    "Django",
    "django-cors-headers",
    "djangorestframework",
    "HttpRunner",
]


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    python_requires='>2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    packages=find_packages(exclude=["migrations"]),
    package_data={
        '': ["README.md"]
    },
    keywords='HTTP api test requests locust',
    install_requires=install_requires,
    extras_require={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3,3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    entry_points={
        'console_scripts': [
            'run=FasterRunner.cli:main_hrun'
        ]
    }
)
