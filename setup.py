import setuptools

# Developer self-reminder for uploading in pypi:
# - install: wheel, twine
# - build  : python setup.py bdist_wheel
# - deploy : twine upload dist/*

with open("README.md", "r") as file:
    long_description = file.read()

with open("requirements.txt", "r") as file:
    requirements = file.read().splitlines()

setuptools.setup(
    name='FedMed',
    version='0.2.0',
    author="Emmanouil (Manios) Krasanakis",
    author_email="maniospas@hotmail.com",
    description="A privacy-aware federated computing scheme to let "
                "non-trusted clients perform statistical analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maniospas/FedMed",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent",
     ],
    install_requires=requirements,
 )