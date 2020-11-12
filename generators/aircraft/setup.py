import setuptools

setuptools.setup(
        name="punch-demo",
    version="1.0.0",
    keywords=["punch"],
    install_requires=[
    "numpy==1.19.4",
    "mlflow==1.12.0",
    "scikit-learn==0.23.2"
    ],    
    packages=setuptools.find_packages(),
)

