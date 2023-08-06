from os import path
from setuptools import setup, find_packages

_here = path.dirname(__file__)


setup(
    name='gg-start',
    version='0.0.5',
    description='Plugin for gg for starting branches',
    long_description=open(path.join(_here, 'README.rst')).read(),
    py_modules=['gg_start'],
    author='Peter Bengtsson',
    author_email='mail@peterbe.com',
    url='https://github.com/peterbe/gg-start',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['gg'],
    entry_points="""
        [gg.plugin]
        cli=gg_start:start
    """,
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock', 'pytest-mock'],
)
