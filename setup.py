from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sportrefpy",
    author="alex kahan",
    author_email="kahanscious@gmail.com",
    version="0.3.0",
    description="Python package to pull sports stats from all major sports leagues.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexkahan/sportrefpy",
    license="MIT",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3"],
    keywords="sports reference stats nba nfl mlb cfb cbb",
    install_requires=[
        "beautifulsoup4 >= 4.10.0",
        "lxml >= 4.8.0",
        "numpy >= 1.22.3",
        "pandas >= 1.4.1",
        "pytest >= 7.1.1",
        "requests >= 2.27.1",
        "urllib3 >= 1.26.9",
        "pyenchant >=3.2.2",
        "html5lib >= 1.1",
    ],
    include_package_data=True,
)
