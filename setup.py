from setuptools import setup
import re

VERSION = None
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: End Users/Desktop",
    "Operating System :: POSIX :: Linux",
    "Environment :: Console",
    "Programming Language :: Python :: 3.6",
    "Topic :: Multimedia :: Sound/Audio"]

if VERSION is None:
    with open("simpletts.py", "r", encoding="utf-8") as stream:
        search_refind = '_{0,2}version_{0,2} = ["\'](\d+\.\d+\.\d+)["\']'
        match = re.search(search_refind, stream.read(), flags=re.IGNORECASE)
        if match:
            VERSION = match.group(1)

setup(
    name='SimpleTTS',
    version=VERSION,
    url='https://github.com/fordetek/SimpleTTS',
    author='Michael Forde',
    author_email='willforde@gmail.com',
    description='A Simple Text to Speach program',
    keywords="tts text speech gtts",
    platforms=["Linux"],
    install_requires=['gtts'],
    classifiers=CLASSIFIERS,
    py_modules=["simpletts"],
    entry_points={"console_scripts": ["simpletts=simpletts:main"]}
)
