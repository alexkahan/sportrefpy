from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sportrefpy',
    author='alex kahan',
    author_email='kahanscious@gmail.com',
    version='0.0.3',
    description='pull sports stats',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/alexkahan/sports_stats',
    license='MIT',
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3"],
    keywords='sports stats nba nfl mlb cfb cbb',
    install_requires=[
        'bs4 >= 0.0.1',
        'lxml >= 4.8.0',
        'numpy >= 1.22.3',
        'pandas >= 1.4.1',
        'pytest >= 7.1.1',
        'requests >= 2.27.1',
        'urllib3 >= 1.26.9',
        'pyenchant >=3.2.2',
    ],
    include_package_data=True,
)