select \*
from jobs_attributes
join jobs on jobs.id = jobs_attributes.job_id
join attributes on attributes.id = jobs_attributes.attribute_id
where jobs.id = 552577
