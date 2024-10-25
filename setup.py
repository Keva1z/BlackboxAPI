from setuptools import setup, find_packages

setup(
    name="blackboxapi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Keva1z",
    author_email="Keva1z@yandex.ru",
    description="Библиотека для работы с Blackbox API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Keva1z/blackboxapi",
)