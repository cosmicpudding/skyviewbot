from setuptools import setup

setup(
    name="SkyviewBot",
    version="0.1.0",
    py_modules=["skyviewbot"],
    entry_points={
        'console_scripts': ['skyviewbot=skyviewbot.cli:main']
    }
)
