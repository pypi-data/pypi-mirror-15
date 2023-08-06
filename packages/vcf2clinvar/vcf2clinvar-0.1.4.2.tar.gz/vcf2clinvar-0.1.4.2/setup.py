from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='vcf2clinvar',
    version='0.1.4.2',
    description='Match a personal genome VCF datafile to ClinVar',
    url='https://github.com/PersonalGenomesOrg/vcf2clinvar',
    author='Personal Genome Project Informatics Group',
    author_email='pgp-informatics@arvados.org',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
    ],

    packages=['vcf2clinvar'],

    # Core dependencies should be listed here (will be installed by pip).
    install_requires=[],

    scripts=['clinvar_report.py'],

)
