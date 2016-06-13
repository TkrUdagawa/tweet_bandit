from setuptools import setup, find_packages

install_requires = [
    'tornado',
    'requests-oauthlib',
    'jubatus'
]


setup(
    name = "twitter_bandit",
    version = "0.0.1",
    packages=find_packages(),
    author = "TkrUdagawa",
    description="This is a library for the example demonstration of jubabandit",
    install_requires = install_requires
)
