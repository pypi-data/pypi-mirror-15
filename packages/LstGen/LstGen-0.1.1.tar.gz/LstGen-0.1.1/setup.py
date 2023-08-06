import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()
long_description = README + "\n\n" + CHANGES
try:
    import pypandoc
    long_description = pypandoc.convert(long_description, 'rst', format='md')
except(IOError, ImportError):
    pass
requires = [
    'lxml',
    'requests'
]

setup(name='LstGen',
    version='0.1.1',
    description='LstGen',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Code Generators"
    ],
    author='Igor Stroh',
    author_email='igor.stroh@rulim.de',
    url='http://github.com/jenner/LstGen',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="lstgen",
    entry_points="""\
    [console_scripts]
    lstgen = lstgen.cli:main
    """
)
