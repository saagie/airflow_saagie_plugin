import logging

from airflow.models import BaseOperator
from querySaagieApi import QuerySaagieApi
from airflow import AirflowException

log = logging.getLogger(__name__)

class SaagieLaunchJobManagerOperator(BaseOperator):
    """
    Launch the specified job in Saagie Manager (v1)
        :param user:        Saagie username

        :param password:    Saagie password

        :param url_saagie:  Saagie platform URL (i.e. https://saagie-manager.prod.saagie.io/)

        :param id_platform: Saagie platform ID

        :param job_id:      Saagie job ID
    """

    def __init__(self, user, password, url_saagie, id_platform, job_id, *args, **kwargs):
        super(SaagieLaunchJobManagerOperator, self).__init__(*args, **kwargs)
        self.user = user
        self.password = password
        self.url_saagie = url_saagie
        self.id_platform = id_platform
        self.job_id = job_id
        self.qsa = QuerySaagieApi(url_saagie, id_platform, user, password)

    def execute(self, context):
        res = self.qsa.run_job(self.job_id)
        if res.status_code != 204:
            raise AirflowException("Did not manage to launch the job, please check your parameters.")
        log.info("Job %s is launched", self.job_id)