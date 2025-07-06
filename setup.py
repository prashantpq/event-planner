from setuptools import setup, find_packages

setup(
    name = 'event_planner',
    version = '0.1.0',
    packages = find_packages(),
    install_requires = [
        'langgraph',
        'langchain',
        'langchain-core',
        'langchain-community',
        'python-dotenv',
        'langchain-groq'

    ],
    author = 'Prashant Sharma',
    author_email = 'prashant.ps9833@gmail.com',
    description = 'A multi-agent AI event & travel planner system',
    long_description = open('README.md').read(),
    url = 'https://github.com/prashantpq/event-planner',
    python_requires = '>=3.7'

)