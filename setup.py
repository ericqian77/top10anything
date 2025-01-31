from setuptools import setup, find_packages

setup(
    name="top10-analytics",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydantic>=2.10.0",
        "tableauhyperapi==0.0.21200",
        "python-dotenv>=0.21.0",
        "tableauserverclient>=0.17.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-asyncio==0.23.6',
        ]
    }
) 