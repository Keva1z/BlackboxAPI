from setuptools import setup, find_packages

setup(
    name="blackboxapi",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.0",
        "aiohttp>=3.10.0",
        "aiohappyeyeballs>=2.4.0",
        "Brotli>=1.1.0", # IDK, Decoding isnt working without it
        "colorama>=0.4.6",
        "propcache>=0.2.0",
        "urllib3>=2.2.0",
        "pydantic>=2.5.2",
        "pyyaml>=6.0.2",
    ],
    python_requires=">=3.8",
    author="Keva1z",
    author_email="Keva1z@yandex.ru",
    description="Python library for Blackbox AI API integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Keva1z/blackboxapi",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)