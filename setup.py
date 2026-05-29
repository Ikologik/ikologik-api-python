from setuptools import find_packages, setup

setup(
    name='ikologikapi',
    version='1.1.70',
    packages=find_packages(include=['ikologikapi*']),
    url='',
    license='MIT',
    author='Ikologik',
    author_email='development@ikologik.com',
    description='Ikologik API',
    install_requires=['requests==2.26.0'],
    python_requires=">=3.9",
)
