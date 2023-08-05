# curio/queue.py
#
# Implementation of a queue object that can be used to communicate
# between tasks.  This is only safe to use within curio. It is not
# thread-safe.

__all__ = [ 'Queue' ]

from collections import deque

from .traps import _wait_on_queue, _reschedule_tasks
from .kernel import kqueue

class Queue(object):
    __slots__ = ('maxsize', '_queue', '_get_waiting', 
                 '_put_waiting', '_join_waiting', '_task_count')

    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self._queue = deque()
        self._get_waiting = kqueue()
        self._put_waiting = kqueue()
        self._join_waiting = kqueue()
        self._task_count = 0

    def empty(self):
        return not self._queue

    def full(self):
        return self.maxsize and len(self._queue) == self.maxsize

    async def get(self):
        if self.empty():
            await _wait_on_queue(self._get_waiting, 'QUEUE_GET')
        result = self._queue.popleft()
        if self._put_waiting:
            await _reschedule_tasks(self._put_waiting, n=1)
        return result

    async def join(self):
        if self._task_count > 0:
            await _wait_on_queue(self._join_waiting, 'QUEUE_JOIN')

    async def put(self, item):
        if self.full():
            await _wait_on_queue(self._put_waiting, 'QUEUE_PUT')
        self._queue.append(item)
        self._task_count += 1
        if self._get_waiting:
            await _reschedule_tasks(self._get_waiting, n=1)

    def qsize(self):
        return len(self._queue)

    async def task_done(self):
        self._task_count -= 1
        if self._task_count == 0 and self._join_waiting:
            await _reschedule_tasks(self._join_waiting, n=len(self._join_waiting))
