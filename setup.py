from setuptools import setup
from setuptools import find_packages


setup(
    name = "py_quick_crawlers",
    version = "0.0.1",
    author = "Vinoth Kumar Kannan",
    author_email = "vdraceil@gmail.com",
    description = "A collection of scrapy spiders to do most required generic " \
        "crawling and wrappers to them hiding the involvement of scrapy " \
        "completely",
    license = "LGPL",
    keywords = "python quick scrapy crawler",
    url = "https://github.com/vdraceil/scrapy-generic-spiders",
    packages = ['py_quick_crawlers'],
    install_requires = [
        "scrapy==1.1.0",
    ],
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "License :: OSI Approved :: LGPL License"
        "Development Status :: 3 - Alpha",
    ],
    zip_safe = True
)
