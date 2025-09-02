"""
The setup.py python file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and other settings.
"""

from setuptools import setup, find_packages
from typing import List 

def get_requirements()->List[str]:
    """
    This function will return the list of requirements.
    """
    try:
        with open("requirements.txt", "r") as file:
            requirements = file.readlines()
            requirements = [req.replace("\n", "") for req in requirements]
            if '' in requirements:
                requirements.remove('')
            if '-e .' in requirements:
                requirements.remove('-e .')
        return requirements
    except FileNotFoundError:
        print(f"requirements.txt not found")
        return []

# print(get_requirements())

setup(
    name="NetworkSecurity",  # The name of the package
    version="0.0.1",  # The version of the package
    author="Asad Hanif",  # The author of the package
    description="A small example package",  # A short description of the package
    author_email="asadhanif3188@gmail.com",  # The author's email address
    packages=find_packages(),  # A list of packages to be included in the distribution
    python_requires=get_requirements(),  # The minimum required Python version
)
