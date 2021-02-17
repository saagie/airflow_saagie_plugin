# Airflow Plugin - Saagie

The Airflow Saagie Plugin lets you interact with Saagie platform from Apache Airflow.

## Installation

You can install this plugin by using the following command:

``` sh
pip install git+https://github.com/saagie/airflow_saagie_plugin.git
```

## How to use?

Here is an example:

``` python
from airflow import DAG
from airflow.operators.python import PythonOperator
from saagie_airflow_plugin.saagie_plugin import SaagieRunJobProjectOperator
import os

password = os.environ['SAAGIE_PASSWORD']

def print_hello():
    return "Hello world!"


dag = DAG('saagie_demo_dag')

run_job_v2 = SaagieRunJobProjectOperator(
    user='baptiste.courbe',
    password=password,
    url_saagie='https://saagie-workspace.prod.saagie.io/',
    id_platform='4',
    realm='saagie',
    job_id='396882c0-25f1-4e8e-9e42-35939cdf4eb3',
    task_id='run_job_v2',
    dag=dag
)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

hello_operator >> run_job_v2
```

Alternatively, connection parameters can be passed to each task directly. This works well when integrated with Airflow variables.

## Operators

### SaagieLaunchJobManagerOperator

This operator launch the specified job in Saagie Manager (V1)
It accepts the following parameters:

```
:param user:        Saagie username
:param password:    Saagie password
:param url_saagie:  Saagie platform URL (i.e. https://saagie-manager.prod.saagie.io/)
:param id_platform: Saagie platform ID
:param job_id:      Saagie job ID
```

### SaagieRunJobProjectOperator

This operator launch the specified job in Saagie Project&Job (V2)
It accepts the following parameters:

```
:param user:        Saagie username
:param password:    Saagie password
:param url_saagie:  Saagie platform URL (i.e. https://saagie-manager.prod.saagie.io/)
:param id_platform: Saagie platform ID
:param realm:       Saagie realm
:param job_id:      Saagie job ID
```

## Sensors

### SaagieJobManagerSensor

Check and wait for the final status of the specified job in Saagie Manager (v1)
It accepts the following parameters:

```
:param user:        Saagie username
:param password:    Saagie password
:param url_saagie:  Saagie platform URL (i.e. https://saagie-manager.prod.saagie.io/)
:param job_id:      Saagie job ID
```

### SaagieRunJobManagerOperator

Run the specified job in Saagie Manager and wait for the final status (v1)
It accepts the following parameters:

```
:param user:        Saagie username
:param password:    Saagie password
:param url_saagie:  Saagie platform URL (i.e. https://saagie-manager.prod.saagie.io/)
:param id_platform: Saagie platform ID
:param job_id:      Saagie job ID
```
