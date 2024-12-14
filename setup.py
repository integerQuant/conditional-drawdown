from setuptools import setup, find_packages

setup(
    name="conditional_drawdown",
    version="0.1.0",
    author="internQuant",
    author_email="cinzeis-rehang.0l@icloud.com",
    description="A Python package for drawdown risk analysis with Conditional Expected Drawdown (CED).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/internQuant/conditional-drawdown",
    project_urls={
        "Source": "https://github.com/internQuant/conditional-drawdown",
        "Documentation": "https://github.com/internQuant/conditional-drawdown/",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "numba",
        "yfinance",
    ],
)
