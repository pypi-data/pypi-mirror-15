from sys import version_info, exit
from setuptools import setup, find_packages
from os import path

if version_info[0] < 3 and version_info[1] < 5:
    exit("Sorry, support only for Python 3.5 and above.")

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tornado-razorpay",
    version="0.1.3",
    description="Razorpay Asynchronous Tornado Python Client",
    url="https://github.com/nkanish2002/tornado-razorpay",
    author="Anish Gupta",
    author_email="nkanish2002@gmail.com",
    license="MIT",
    install_requires=["tornado>4"],
    package_dir={'tornado_razorpay': 'tornado_razorpay'},
    packages=find_packages(),
    keywords='razorpay payment gateway india tornado async',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
