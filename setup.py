"""
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as fl:
    license = fl.read()

with open("requirements.txt", "r") as fr:
    requirements = fr.read()

setuptools.setup(
    name="DCViewer-PsyJim",
    version="0.2.0",
    author="Jim Acosta",
    author_email="jimgerardo@outlook.com",
    description="A viewer for data cubes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=license,
    url="https://github.com/PsyJim/DCViewer",
    packages=setuptools.find_packages(),
    install_requires=[requirements],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)