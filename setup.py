from setuptools import setup, find_packages

setup(
    name='LBMSimulationInterface',
    version='1',
    packages=find_packages(),
    install_requires=[
        'numpy', 'pyvista'
    ],
    # Additional metadata about your package
    author='Calum Mallorie',
    author_email='calum.mallorie@gmail.com',
    description='A python interface for BioFM LBM simulations',
)