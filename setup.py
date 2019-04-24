from pathlib import Path

from setuptools import find_packages
from setuptools import setup


DESCRIPTION = (
    "respy is a Python package for the simulation and estimation of a "
    "prototypical finite-horizon dynamic discrete choice model. "
)

README = Path("README.rst").read()

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/OpenSourceEconomics/respy/issues",
    "Documentation": "https://respy.readthedocs.io/en/latest",
    "Source Code": "https://github.com/OpenSourceEconomics/respy",
}


def setup_package():
    """First steps towards a reliable build process."""
    metadata = dict(
        name="respy",
        packages=find_packages(),
        package_data={"respy": ["tests/resources/*", "pre_processing/base_spec.csv"]},
        version="1.2.0",
        description=DESCRIPTION,
        long_description=README,
        author="Philipp Eisenhauer",
        author_email="eisenhauer@policy-lab.org",
        url="https://respy.readthedocs.io/en/latest/",
        project_urls=PROJECT_URLS,
        license="MIT",
        keywords=["Economics", "Dynamic Discrete Choice Model"],
        classifiers=[
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
        ],
        install_requires=[
            "numba>=0.43",
            "pandas>=0.24",
            "scipy>=0.19",
            "statsmodels>=0.9",
            "pytest>=4.0",
            "pyaml",
        ],
        platforms="any",
        include_package_data=True,
        zip_safe=False,
    )

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
