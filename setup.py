from setuptools import setup, find_packages

setup(
    name='azure_lightning_flask',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['azure_lightning_flask=azure_lightning_flask.__main__:main'],
    },
    setup_requires=[
        'setuptools',
    ],
    install_requires=open('requirements.txt').readlines()
)