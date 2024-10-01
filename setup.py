from setuptools import setup, find_packages
import os

# Read the contents of README.md for the long_description
def read_long_description():
    here = os.path.abspath(os.path.dirname(__file__))
    readme_path = os.path.join(here, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='ukpostcodeio',
    version='1.0.0',
    description='A Python client for the Postcodes.io API used for UK postcodes',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',  # Specify Markdown for README
    author='Rohit Yelukati Mahendra',
    author_email='rohityelukati@gmail.com',
    url='https://github.com/ymrohit/ukpostcodeio',
    packages=find_packages(),
    install_requires=[
        'requests>=2.23.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',  # Specify supported versions
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',  # Update if using a different license
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.7',  # Specify minimum Python version
    include_package_data=True,  # Include non-code files as specified in MANIFEST.in
    keywords='postcode uk postcodes.io api client',  # Relevant keywords
    license='MIT',  # Update if using a different license
)