from setuptools import setup, find_packages

setup(
    name="CarRentalSystem",
    version="1.0.0",
    description="Python app with GUI connecting to PostgreSQL",
    author="Przemysław Ryś",
    packages=find_packages(),  # Automatycznie wykrywa wszystkie pakiety
    install_requires=["psycopg2"],
    entry_points={
        "console_scripts": [
            "car_rental_system=app:main",
        ]
    },
    include_package_data=True,
)