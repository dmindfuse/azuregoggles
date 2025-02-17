from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="azure_blob_browser",
    version="1.0.0",
    author="Tom Ceyssens",
    description="A Linux shell Azure Blob Storage browser and blob downloader using the Python Cement framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "cement",
        "azure-cli",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
    entry_points={
        'console_scripts': [
            'azuregoggles=main:run',
        ],
    },
)
