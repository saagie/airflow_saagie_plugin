import logging
import json

from airflow.sensors.base import BaseSensorOperator
from querySaagieApi import QuerySaagieApi
from airflow import AirflowException

log = logging.getLogger(__name__)

class SaagieJobManagerSensor(BaseSensorOperator):
    """
    Check and wait for the final status of the specified job in Saagie Manager (v1)
        :param user:        Saagie username

        :param password:    Saagie password

        :param url_saagie:  Saagie platform URL (i.e. https://saagie-manager.prod.saagie.io/)

        :param id_platform: Saagie platform ID

        :param job_id:      Saagie job ID
    """

    def __init__(self, user, password, url_saagie, id_platform, job_id, *args, **kwargs):
        super(SaagieJobManagerSensor, self).__init__(*args, **kwargs)
        self.user = user
        self.password = password
        self.url_saagie = url_saagie
        self.id_platform = id_platform
        self.job_id = job_id
        self.qsa = QuerySaagieApi(url_saagie, id_platform, user, password)

    def poke(self, context):
        res = self.qsa.get_job_detail(self.job_id)

        if not res.status_code == 200:
            log.info('Bad HTTP response: %s', res.status_code)
            return False

        state = json.loads(res.text)['last_state']['state']
        last_task_status = json.loads(res.text)['last_state']['lastTaskStatus']
        log.info('Job currently %s', state)

        if state != 'STOPPED':
            return False
        elif last_task_status != 'SUCCESS':
            return AirflowException("Final status : %s", last_task_status)
        else:
            # Go to next operator
            return True
