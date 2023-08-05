"""Seriously - a Python-based golfing language"""

from setuptools import setup, find_packages

setup(
    name='seriously',

    version='2.0.2',

    description='A Python-based golfing language',
    long_description='Seriously is a Python-based golfing language. See the GitHub page for more details.',

    url='https://github.com/Mego/Seriously',

    author='Mego',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='codegolf recreational',

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'seriously=seriously:main',
        ],
    },
)