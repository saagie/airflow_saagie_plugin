import logging

from airflow.models import BaseOperator
from querySaagieApi import QuerySaagieApiProject
from airflow import AirflowException

log = logging.getLogger(__name__)

class SaagieRunJobProjectOperator(BaseOperator):
    """
    Launch the specified job in Saagie Project&Job (v2)
        :param user:        Saagie username

        :param password:    Saagie password

        :param url_saagie:  Saagie platform URL (i.e. https://saagie-manager.prod.saagie.io/)

        :param id_platform: Saagie platform ID

        :param realm:       Saagie realm

        :param job_id:      Saagie job ID
    """

    def __init__(self, user, password, url_saagie, id_platform, realm, job_id, *args, **kwargs):
        super(SaagieRunJobProjectOperator, self).__init__(*args, **kwargs)
        self.user = user
        self.password = password
        self.url_saagie = url_saagie
        self.id_platform = id_platform
        self.realm = realm
        self.job_id = job_id
        self.qsa = QuerySaagieApiProject(url_saagie, id_platform, user, password, realm)

    def execute(self, context):
        status = self.qsa.run_job_callback(self.job_id)
        if status in ["FAILED", "KILLED"]:
            raise AirflowException("Job %s finished with %s statuts" % (self.job_id, status))
        log.info("Job %s finished with %s statuts" % (self.job_id, status))