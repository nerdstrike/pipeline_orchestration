from setuptools import find_packages, setup
from distutils.util import convert_path

version_path = convert_path('pipeline_orchestrator/version.py')
namespace = {}
with open(version_path) as ver_file:
    exec(ver_file.read(), namespace)

setup(
    name='pipeline orchestrator',
    version=namespace['__version__'],
    packages=find_packages(exclude=['tests']),
    license='Apache License 2.0',
    author='Kieron Taylor',
    author_email='kt19@sanger.ac.uk',
    description='Work allocation and tracking for portable pipelines',
    install_requires=[
        'aiomysql',
        'aiosqlite',
        'databases',
        'fastapi',
        'pymysql',
        'sqlalchemy',
        'ujson',
        'ml-warehouse @ git+https://github.com/wtsi-npg/ml-warehouse-python@0.1.0'
    ],
    tests_require=[
        'pytest',
        'pytest-it'
    ]
)
