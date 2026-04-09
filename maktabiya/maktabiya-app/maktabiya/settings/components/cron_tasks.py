# https://django-q.readthedocs.io ( not maintained anymore django-q==1.3.9)
# https://django-q2.readthedocs.io (migrating on this django-q2)
# Need for executing tasks
# import psutil

Q_CLUSTER_DEFAULT_QUEUE = "DefaultTasks"
Q_CLUSTER_LONG_QUEUE = "LongTasks"
Q_CLUSTER_SHORT_QUEUE = "ShortTasks"

WORKERS = 4  # or psutil.cpu_count(logical=True)

Q_CLUSTER = {
    # Label for admin interface
    "label": "Automation Hub",
    # Default Qcluster name
    "name": Q_CLUSTER_DEFAULT_QUEUE,
    # database connection to use for the ORM broker
    "orm": "default",
    # django-redis connection name for the Redis broker
    #'django_redis': 'default',
    # redis as alternative broker
    # 'redis': {'host': 'redis','port': 6379,'db': 0,'password': None},
    # number of workers
    "workers": WORKERS,
    # how many times a task will be retried if it fails
    "max_attempts": 1,
    # queue polling interval (in seconds) for database brokers
    "poll": 2,
    # kill tasks after X seconds
    "timeout": 20,
    # time in seconds to wait before retrying a failed task
    "retry": 30,
    "compress": True,
    # 0 for unlimited
    "save_limit": 0,
    # Sets the number of processor each worker can use, requires psutil
    "cpu_affinity": 2,
    # don't run old task missed in the past
    "catch_up": False,
    # multi qclusters queue
    "ALT_CLUSTERS": {
        Q_CLUSTER_LONG_QUEUE: {
            "timeout": 3000,
            "retry": 3600,
            "max_attempts": 2,
        },
        Q_CLUSTER_SHORT_QUEUE: {
            "timeout": 10,
            "max_attempts": 1,
        },
    },
}
