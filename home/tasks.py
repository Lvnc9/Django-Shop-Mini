from bucket import bucket
from celery import shared_task

# NOTE:remember to use celery you need to async it
def all_bucket_objects_task():
    result = bucket.get_objects()
    if result['KeyCount']:
        return result['Contents']
    return None


# running this task as async
@shared_task
def delete_object_task(key):
    bucket.delte_object(key)
 
@shared_task
def download_object_task(key):
    bucket.download_object(key)
