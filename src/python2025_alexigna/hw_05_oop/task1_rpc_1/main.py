# /Users/alexigna/projects/python2025-alexigna/src/python2025_alexigna/hw_05_oop/task1_redis_rpc_1
# запускаем с default очередью
# rq worker
# передаем функцию -> меняем на строку, отвязывая клиент от сервера
import time

from redis import Redis
from rq import Queue

from python2025_alexigna.hw_05_oop.task1_rpc_1.utils import hello

redis = Redis()
queue = Queue(connection=redis)

job = queue.enqueue(
    f=hello,
    user="admin",
    count=3,
)
print(redis.hget(f"rq:job:{job.id}", "description").decode())

print(job.result)
time.sleep(2)
print(job.result)


# что хотим: убрать все взаимодействие и предоставить контекстный менеджер
# для взаимодействия вида
#
# with RPC() as rpc:
#     result = rpc.some_server_function(args, kwargs)
#     print(result)
