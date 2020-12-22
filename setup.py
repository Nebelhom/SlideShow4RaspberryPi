import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slideshow-Nebelhom",
    version="0.0.1",
    author="Johannes Vogel",
    author_email="nebelhom@hotmail.com",
    description="A simple Slideshow for Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nebelhom/SlideShow4RaspberryPi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
