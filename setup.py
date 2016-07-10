from setuptools import setup
from setuptools import find_packages


setup(
    name = "py-quick-crawlers",
    version = "0.0.1",
    author = "Vinoth Kumar Kannan",
    author_email = "vdraceil@gmail.com",
    description = "Python APIs wrapping generic Scrapy crawlers"
    license = "MIT",
    keywords = "python quick scrapy web crawler",
    url = "https://github.com/vdraceil/py-quick-crawlers",
    packages = find_packages(),
    install_requires = [
        "scrapy==1.1.0",
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Developement",
        "Topic :: Web Crawling",
        "License :: OSI Approved :: MIT License",
    ],
    zip_safe = True
)
