from setuptools import setup, find_packages

setup(
    name='azure_lightning_flask',
    version='0.0.1',
    author='Hayden Demerson',
    description='Lightning deployment strategy on Azure with Flask',
    long_description=open('README.rst').read(),
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Framework :: Flask',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['azure_lightning_flask=azure_lightning_flask.__main__:main'],
    },
    setup_requires=[
        'setuptools',
        'setuptools-git',
        'wheel',
        'nose>=1.3'
    ],
    install_requires=open('requirements.txt').readlines(),
    tests_require=[
        'mock>=2.0.0'
    ],
    test_suite = 'nose.collector'
)