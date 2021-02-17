import logging
import json

from airflow.sensors.base import BaseSensorOperator
from querySaagieApi import QuerySaagieApi
from airflow import AirflowException

log = logging.getLogger(__name__)

class SaagieRunJobManagerOperator(BaseSensorOperator):
    """
    Run the specified job in Saagie Manager and wait for the final status (v1)
        :param user:        Saagie username

        :param password:    Saagie password

        :param url_saagie:  Saagie platform URL (i.e. https://saagie-manager.prod.saagie.io/)

        :param id_platform: Saagie platform ID

        :param job_id:      Saagie job ID
    """

    def __init__(self, user, password, url_saagie, id_platform, job_id, *args, **kwargs):
        super(SaagieRunJobManagerOperator, self).__init__(*args, **kwargs)
        self.user = user
        self.password = password
        self.url_saagie = url_saagie
        self.id_platform = id_platform
        self.job_id = job_id
        self.qsa = QuerySaagieApi(url_saagie, id_platform, user, password)
        self.launched = False

    def poke(self, context):
        if not self.launched:
            res_launch = self.qsa.run_job(self.job_id)
            if res_launch.status_code != 204:
                raise AirflowException("Did not manage to launch the job, please check your parameters.")
            log.info("Job %s is launched", self.job_id)
            self.launched = True

        res_status = self.qsa.get_job_detail(self.job_id)

        if not res_status.status_code == 200:
            log.info('Bad HTTP response: %s', res_status.status_code)
            return False

        state = json.loads(res_status.text)['last_state']['state']
        last_task_status = json.loads(res_status.text)['last_state']['lastTaskStatus']
        log.info('Job currently %s', state)

        if state != 'STOPPED':
            return False
        elif last_task_status != 'SUCCESS':
            return AirflowException("Final status : %s", last_task_status)
        else:
            # Go to next operator
            return True