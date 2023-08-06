from setuptools import setup

setup(
    name='bashup',
    version='2.0.2',
    packages=(
        'bashup',
        'bashup.compile',
        'bashup.compile.elements'),
    url='https://github.com/themattrix/bashup',
    license='MIT',
    author='Matthew Tardiff',
    author_email='mattrix@gmail.com',
    install_requires=(
        'docopt',
        'Jinja2',
        'pyparsing',
        'temporary>=3,<4',),
    tests_require=(
        'contextlib2',
        'mock',
        'pathlib2',
        'pytest',
        'temporary>=3,<4'),
    entry_points={
        'console_scripts': (
            'bashup = bashup.__main__:main',)},
    description=(
        'A (toy) language that compiles to bash.'),
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'))
