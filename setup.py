from setuptools import setup, find_packages

setup(
    name='UllmanSubgraph',
    version='1.0.0',
    author='Kalvin Dobler',
    description='Implementation of Ullman’s Subgraph Isomorphism Test',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['numpy', 'networkx'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)