from setuptools import find_packages, setup # find package finds our created package

# sets up the meta data for the package
setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Adarsh Potanpalli",
    author_email="p.adarsh.24072001@gmail.com",
    install_requires=['openai','python-dotenv','streamlit','langchain', 'langchain-community', 'langchain-openai','PyPDF2'],
    packages=find_packages()
)