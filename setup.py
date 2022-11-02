import setuptools
import os

print(os.getcwd())
print(os.listdir())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = []
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="blockchain-tutorial-python",
    version="0.0.1",
    author="Daniel Salgado Rojo",
    description="Introduction to blockchain and blockchain data with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsalgador/blockchain-tutorial-python",
    install_requires=install_requires,
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
