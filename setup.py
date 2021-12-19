from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='pyjudi_tjpr',
    version='1.0.2',
    url='',
    license='MIT License',
    author='Viiict0r',
    author_email='victorh.cepil@hotmail.com',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords=['Projudi tjpr', 'Projudi paraná', 'Projudi crawler'],
    description=u'Helper para efetuar login no sistema do projudi tjpr',
    packages=['pyjudi_tjpr'],
    install_requires=[
        'onetimepass>=1.0.1,<2',
        'requests>=2.26.0,<3',
        'beautifulsoup4>=4.10.0,<5'
    ]
)