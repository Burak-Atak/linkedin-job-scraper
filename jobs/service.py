import json
import logging
import random
import time
from datetime import datetime
from django.utils.timezone import make_aware
from django.conf import settings
from linkedin_api import Linkedin
from address.service import CityService
from company.service import CompanyService
from jobs.models import Job
from requests.cookies import RequestsCookieJar

logger = logging.getLogger(__name__)


class JobsService:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            username = settings.LINKEDIN_USERNAME
            password = settings.LINKEDIN_PASSWORD
            cookie_dict = json.loads(settings.LINKEDIN_COOKIES)
            cookies = RequestsCookieJar()
            for cookie in cookie_dict:
                cookies.set(cookie, cookie_dict[cookie])
            cls.instance = super(JobsService, cls).__new__(cls)
            cls.api = Linkedin(username, password, cookies=cookies)
        return cls.instance

    def bulk_update_status(self, data):
        job_ids = data.get('job_ids')
        status = data.get('status')
        Job.objects.filter(id__in=job_ids).update(status=status)

        return {"message": "Status updated successfully"}

    @classmethod
    def create_job(cls, data):
        city = CityService.get_or_create_city(data.pop('city'))
        company = CompanyService.get_or_create_company(data.pop('company'))
        linkedin_job_id = data.pop('linkedin_job_id')
        job, created = Job.objects.get_or_create(linkedin_job_id=linkedin_job_id, defaults={
            **data,
            'city': city,
            'company': company
        })
        return job

    @classmethod
    def get_job_details(cls, job_id):
        # job = self.api.get_job(job_id)
        url = f"/jobs/jobPostings/{job_id}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65&topN=1&topNRequestedFlavors=List(TOP_APPLICANT,IN_NETWORK,COMPANY_RECRUIT,SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)"
        job = cls.api._fetch(url)
        job = job.json()
        return cls.parse_job_details(job)

    @classmethod
    def parse_job_details(cls, job_details):
        company = {}
        title = job_details.get('title')
        description = job_details.get('description').get('text')
        work_type = job_details.get('workplaceTypes')[0].split(":")[-1] if job_details.get('workplaceTypes') else None
        linkedin_job_id = job_details.get('jobPostingId')
        url = f"https://www.linkedin.com/jobs/view/{linkedin_job_id}"
        date_posted_timestamp = job_details.get('listedAt')  # timestamp
        date_posted = datetime.fromtimestamp(date_posted_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        date_posted = make_aware(datetime.strptime(date_posted, '%Y-%m-%d %H:%M:%S'))
        city = job_details.get('formattedLocation')
        applies = job_details.get('applies')
        """include_elements = job_details.get('included', [])
        for included in include_elements:
            element_type = included.get('$type')
            if element_type == "com.linkedin.voyager.organization.Company":
                company = included.get('name')"""
        company_details = job_details.get('companyDetails')
        if company_details:
            key = list(company_details.keys())[0]
            company_name = company_details[key].get("companyResolutionResult").get("name")
            logos = (company_details[key].get("companyResolutionResult")
                     .get("logo").get('image')
                     .get('com.linkedin.common.VectorImage')
                     .get('artifacts'))

            logo_path = sorted(logos, key=lambda x: x.get('width'))[0]["fileIdentifyingUrlPathSegment"]
            root_url = (company_details[key].get("companyResolutionResult")
                        .get("logo").get('image')
                        .get('com.linkedin.common.VectorImage')
                        .get('rootUrl'))
            logo_url = f"{root_url}{logo_path}"
            company = {
                'name': company_name,
                'logo': logo_url
            }

        return {
            'title': title,
            'description': description,
            'work_type': work_type,
            'linkedin_job_id': linkedin_job_id,
            'url': url,
            'date_posted': date_posted,
            'city': city,
            'company': company,
            'applies': applies
        }

    @classmethod
    def scrape_jobs(cls, keywords, **kwargs):
        is_continue = True
        listed_at = kwargs.pop('listed_at', 24 * 60 * 60)
        limit = kwargs.pop('limit', 25)
        offset = kwargs.pop('offset', 0)
        jobs = cls.api.search_jobs(keywords, listed_at=listed_at, limit=limit, offset=offset, **kwargs)
        if not jobs:
            is_continue = False

        for job in jobs:
            try:
                job_id = job.get('trackingUrn').split(':')[-1]
                job_details = cls.get_job_details(job_id)
                job = cls.create_job(job_details)
                time.sleep(random.uniform(5, 8))
            except Exception as e:
                logger.error(f"Error creating job: Job id: {job_id}\n{e}", exc_info=True)

        return is_continue
