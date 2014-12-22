from __future__ import absolute_import

from .base import QueueInterface
from Queue import PriorityQueue

class QueueBackend(QueueInterface):
    def __init__(self, unique=False, **kwargs):
        super(QueueBackend, self).__init__(unique, **kwargs)
        self.queue_object = PriorityQueue()
        self.unique = unique
        self.unique_dict = {}

    def put(self, task, priority):
        if self.unique:
            key = unique_key(task)
            if key in self.unique_dict:
                return
            self.unique_dict[key] = True
        self.queue_object.put((priority, task))

    def get(self, timeout):
        priority, task = self.queue_object.get(True, timeout)
        if self.unique:
            key = unique_key(task)
            del self.unique_dict[key]
        return task

    def size(self):
        return self.queue_object.qsize()

def unique_key(task):
    return '%s:%s' % (task.name, task.url)
