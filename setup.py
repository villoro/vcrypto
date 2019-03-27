import io
from setuptools import setup

setup(
    name="v_crypt",
    version="1.0.1",
    author="Arnau Villoro",
    author_email="arnau@villoro.com",
    packages=["v_crypt"],
    include_package_data=True,
    license="MIT",
    description=("Utility to easily store password/secrets."),
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/villoro/v-crypt",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)
