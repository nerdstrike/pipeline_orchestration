from setuptools import find_packages, setup

setup(
    name='pipeline orchestrator',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    license='Apache License 2.0',
    author='Kieron Taylor',
    author_email='kt19@sanger.ac.uk',
    description='Work allocation and tracking for portable pipelines',
    install_requires=[
        'pymysql',
        'sqlalchemy',
        'fastapi',
        'ml-warehouse @ git+https://github.com/wtsi-npg/ml-warehouse-python@0.1.0'
    ],
    tests_require=[
        'pytest',
        'pytest-it'
    ]
)