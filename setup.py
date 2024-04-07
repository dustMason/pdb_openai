from setuptools import setup, find_packages
from pdb_openai import __version__

setup(
    name="pdb_openai",
    version=__version__,
    author="Jordan Sitkin",
    author_email="jordan@fiftyfootfoghorn.com",
    description="A python debugger with OpenAI integrations",
    long_description=open('readme.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dustmason/pdb_openai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "openai",
    ],
)
