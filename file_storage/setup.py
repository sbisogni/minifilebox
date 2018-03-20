from setuptools import setup, find_packages

setup(
    name='file_storage',
    version='0.3',
    description='MinifileBox File Storage',
    url='https://github.com/sbisogni/minifilebox',
    author='Simone Bisogni',
    author_email='simone.bisogni@yahoo.it',
    packages=find_packages(),
    install_requires=['cassandra-driver', 'requests']
)
