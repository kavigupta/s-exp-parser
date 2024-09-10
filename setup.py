import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s-exp-parser",
    version="1.4.0",
    author="Kavi Gupta",
    author_email="s_exp_parser@kavigupta.org",
    description="S expression parser for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavigupta/s-exp-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=["attrs>=19.3.0"],
)
