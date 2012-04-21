from setuptools import setup

setup(
    name='tjrj-processos',
    version='0.1dev',
    packages=['tjrj',],
    include_package_data = True,
    license='GPLv2',
    long_description=open('README').read(),

    entry_points = {
        'console_scripts': [
            'tjrj = tjrj.cli:run',
        ],
    }
)
