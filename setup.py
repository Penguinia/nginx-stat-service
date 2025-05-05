from setuptools import setup, find_packages

setup(
    name="nginx-stat-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'python-dateutil>=2.8.0',
    ],
    entry_points={
        'console_scripts': [
            'nginx-stat=app.main:main',
        ],
    },
    python_requires='>=3.8',
)