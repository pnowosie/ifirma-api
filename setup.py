import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pnowosie.ifirma-api",  # Replace with your own username
    version="1.3.0",
    author="Paweł Nowosielski",
    author_email="nowosielski@gmail.com",
    description="IFirma API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pnowosie/ifirma-api",
    packages=setuptools.find_packages(),
    install_requires=["requests", "pyyaml"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
