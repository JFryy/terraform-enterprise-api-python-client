import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyterprise",
    version="0.0.2",
    author="James Fotherby",
    author_email="fotherby1@gmail.com",
    description="A small client library for the Terraform Enterprise REST API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fotherbyy/PyTerprise",
    install_requires=['requests'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
