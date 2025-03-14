from setuptools import setup, find_packages

setup(
    name="ai_roast_machine",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "pillow>=10.0.0",
        "nltk>=3.8.0",
        "rich>=13.0.0",
        "seaborn>=0.12.0",
        "fastapi>=0.95.0",
        "uvicorn>=0.22.0",
    ],
    python_requires=">=3.8",
) 