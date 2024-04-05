from setuptools import find_packages, setup

setup(
    name="dagster_omop",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "dagster",
        "dagster-dbt",
        "dbt-postgres",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)