from setuptools import setup

setup(
    name="alone",
    version="0.1",
    py_modules=["alone"],
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        alone=alone.main:cli
    """,
)
