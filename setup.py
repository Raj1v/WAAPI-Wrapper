from setuptools import setup, find_packages

setup(
    name="waapi_wrapper",
    version="0.3.3",
    packages=find_packages(),
    install_requires=["pydantic>=2.0"],
    author="Raj1v",
    description="A Python wrapper for the WAAPI Whatsapp API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Raj1v/WAAPI-Wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_data={"waapi_wrapper": ["*.json"]},
)
