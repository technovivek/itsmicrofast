from celery import Celery

celery_app = Celery()

def myfn():
    print("inside myfn")


@celery_app.task(name = "mytask",bind = True, on_failure = myfn)
def myfunction(self):
    try:
        print("here")
        raise Exception("from here")
    except Exception as e:
        raise self.retry(exc = e, max_retries = 2)

