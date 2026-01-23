'''File helping to package the projects as packages/libraries
Used by setuptools to define configuration such as metadata, dependencies.
Executed when everything is ready.'''

from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    '''Returns list of requirements'''
    requirements:List[str] = []
    
    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirements.append(requirement)

    except FileNotFoundError:                
        print("File not found")

    return requirements

setup(
    name="Network_Security",
    version = "0.0.1",
    author = "Dhruv Tiwari",
    author_email = "tiwaridhruv15@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)    