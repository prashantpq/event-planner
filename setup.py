from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path : str) -> List[str]:
    """
    This function will return the list of requirements
    """

    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [r.strip() for r in requirements]
    return requirements


setup(
    name = 'event_planner',
    version = '0.0.1',
    packages = find_packages(),
    install_requires = get_requirements('./requirements.txt'),
    author = 'Prashant Sharma',
    author_email = 'prashant.ps9833@gmail.com',
    description = 'A multi-agent AI event & travel planner system',
    long_description = open('README.md').read(),
    url = 'https://github.com/prashantpq/event-planner',
    python_requires = '>=3.7'

)