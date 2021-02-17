from setuptools import setup, find_packages

setup(
    name='airflow_saagie_plugin',
    version='0.1',
    description='Airflow plugin for Saagie plateform',
    url='https://www.saagie.com/',
    author='Service team',
    license='GLWTPL',
    packages=find_packages(),
    install_requires=[
          'querySaagieApi'
      ],
    dependency_links=[
        'git+https://github.com/saagie/api-saagie#egg=querySaagieApi'
      ],
    entry_points = {
        'airflow.plugins': [
            'saagie_plugin = airflow_saagie_plugin:SaagiePlugin'
        ]
    },
    zip_safe=False
)