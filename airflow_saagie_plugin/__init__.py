from airflow.plugins_manager import AirflowPlugin

from .operators.saagie_launch_job_manager_operator import SaagieLaunchJobManagerOperator
from .operators.saagie_run_job_project_operator import SaagieRunJobProjectOperator
from .sensors.saagie_job_manager_sensor import SaagieJobManagerSensor
from .sensors.saagie_run_job_manager_operator import SaagieRunJobManagerOperator

class SaagiePlugin(AirflowPlugin):
    name = "saagie_plugin"
    operators = [SaagieLaunchJobManagerOperator, SaagieRunJobProjectOperator]
    sensors = [SaagieJobManagerSensor, SaagieRunJobManagerOperator]
