from setuptools import setup, find_packages

setup(
    name="SkyviewBot",
    description="Script to download image from SkyView and post it to Slack.",
    license="MIT License",
    author="V.A. Moss and T.J. Dijkema",
    author_email="vmoss.astro@gmail.com",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['skyviewbot=skyviewbot.cli:main']
    }
)
