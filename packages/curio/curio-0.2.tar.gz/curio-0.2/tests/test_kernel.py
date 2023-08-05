# test_kernel.py

import time
from curio import *

def test_hello(kernel):
    results = []
    async def hello():
        results.append('hello')

    kernel.run(hello())
    assert results == [ 'hello' ]

def test_sleep(kernel):
    results = []
    async def main():
          results.append('start')
          await sleep(0.5)
          results.append('end')

    start = time.time()
    kernel.run(main())
    end = time.time()
    assert results == [
            'start',
            'end',
            ]
    elapsed = end-start
    assert elapsed > 0.5

def test_sleep_cancel(kernel):
    results = []

    async def sleeper():
        results.append('start')
        try:
            await sleep(1)
            results.append('not here')
        except CancelledError:
            results.append('cancelled')

    async def main():
        task = await spawn(sleeper())
        await sleep(0.5)
        await task.cancel()

    kernel.run(main())
    assert results == [
            'start',
            'cancelled',
            ]


def test_sleep_timeout(kernel):
    results = []

    async def sleeper():
        results.append('start')
        try:
            await timeout_after(0.5, sleep(1))
            results.append('not here')
        except TaskTimeout:
            results.append('timeout')

    async def main():
        task = await spawn(sleeper())
        await task.join()

    kernel.run(main())
    assert results == [
            'start',
            'timeout',
            ]

def test_sleep_ignore_timeout(kernel):
    results = []

    async def sleeper():
        results.append('start')
        if await ignore_after(0.5, sleep(1)) is None:
            results.append('timeout')

        async with ignore_after(0.5) as s:
            await sleep(1)

        if s.result is None:
            results.append('timeout2')


    async def main():
        task = await spawn(sleeper())
        await task.join()

    kernel.run(main())
    assert results == [
            'start',
            'timeout',
            'timeout2',
            ]

def test_sleep_notimeout(kernel):
    results = []

    async def sleeper():
        results.append('start')
        try:
            await timeout_after(1.5, sleep(1))
            results.append('here')
        except TaskTimeout:
            results.append('not here')

        await sleep(1)
        results.append('here2')

    async def main():
        task = await spawn(sleeper())
        await task.join()

    kernel.run(main())
    assert results == [
            'start',
            'here',
            'here2'
            ]

def test_task_join(kernel):
    results = []

    async def child():
        results.append('start')
        await sleep(0.5)
        results.append('end')
        return 37

    async def main():
        task = await spawn(child())
        await sleep(0.1)
        results.append('joining')
        r = await task.join()
        results.append(r)

    kernel.run(main())
    assert results == [
            'start',
            'joining',
            'end',
            37
            ]

def test_task_join_error(kernel):
    results = []

    async def child():
        results.append('start')
        int('bad')

    async def main():
        task = await spawn(child())
        await sleep(0.1)
        results.append('joining')
        try:
            r = await task.join()
            results.append(r)
        except TaskError as e:
            results.append('task fail')
            results.append(type(e))
            results.append(type(e.__cause__))

    kernel.run(main())
    assert results == [
            'start',
            'joining',
            'task fail',
            TaskError,
            ValueError,
            ]

def test_task_cancel(kernel):
    results = []

    async def child():
        results.append('start')
        try:
            await sleep(0.5)
            results.append('end')
        except CancelledError:
            results.append('cancelled')

    async def main():
        task = await spawn(child())
        results.append('cancel start')
        await sleep(0.1)
        results.append('cancelling')
        await task.cancel()
        results.append('done')

    kernel.run(main())
    assert results == [
            'start',
            'cancel start',
            'cancelling',
            'cancelled',
            'done',
            ]


def test_task_cancel_join(kernel):
    results = []

    async def child():
        results.append('start')
        await sleep(0.5)
        results.append('end')

    async def main():
        task = await spawn(child())
        results.append('cancel start')
        await sleep(0.1)
        results.append('cancelling')
        await task.cancel()
        # Try joining with a cancelled task. Should raise a TaskError
        try:
            await task.join()
        except TaskError as e:
            if type(e.__cause__) == CancelledError:
                results.append('join cancel')
            else:
                results.append(str(e.__cause__))
        results.append('done')

    kernel.run(main())
    assert results == [
            'start',
            'cancel start',
            'cancelling',
            'join cancel',
            'done',
            ]


def test_task_cancel_join_wait(kernel):
    results = []

    async def child():
        results.append('start')
        await sleep(0.5)
        results.append('end')

    async def canceller(task):
        await sleep(0.1)
        results.append('cancel')
        await task.cancel()

    async def main():
        task = await spawn(child())
        results.append('cancel start')
        await spawn(canceller(task))
        try:
            results.append('join')
            await task.join()     # Should raise TaskError... with CancelledError as cause
        except TaskError as e:
            if type(e.__cause__) == CancelledError:
                results.append('join cancel')
            else:
                results.append(str(e.__cause__))
        results.append('done')

    kernel.run(main())
    assert results == [
            'start',
            'cancel start',
            'join',
            'cancel',
            'join cancel',
            'done',
            ]

def test_task_child_cancel(kernel):
    results = []

    async def child():
        results.append('start')
        try:
            await sleep(0.5)
            results.append('end')
        except CancelledError:
            results.append('child cancelled')

    async def parent():
        try:
             child_task = await spawn(child())
             await sleep(0.5)
             results.append('end parent')
        except CancelledError:
            await child_task.cancel()
            results.append('parent cancelled')

    async def grandparent():
        try:
            parent_task = await spawn(parent())
            await sleep(0.5)
            results.append('end grandparent')
        except CancelledError:
            await parent_task.cancel()
            results.append('grandparent cancelled')

    async def main():
        task = await spawn(grandparent())
        await sleep(0.1)
        results.append('cancel start')
        await sleep(0.1)
        results.append('cancelling')
        await task.cancel()
        results.append('done')

    kernel.run(main())

    assert results == [
            'start',
            'cancel start',
            'cancelling',
            'child cancelled',
            'parent cancelled',
            'grandparent cancelled',
            'done',
            ]

def test_task_ready_cancel(kernel):
    # This tests a tricky corner case of a task cancelling another task that's also 
    # on the ready queue.
    results = []

    async def child():
        try:
            results.append('child sleep')
            await sleep(1.0)
            results.append('child slept')
            await sleep(1.0)
            results.append('should not see this')
        except CancelledError:
            results.append('child cancelled')

    async def parent():
        task = await spawn(child())
        results.append('parent sleep')
        await sleep(0.5)
        results.append('cancel start')
        await task.cancel()
        results.append('cancel done')

    async def main():
        task = await spawn(parent())
        await sleep(0.1)
        time.sleep(1)      # Forced block of the event loop. Both tasks should awake when we come back
        await sleep(0.1)

    kernel.run(main())

    assert results == [
            'child sleep',
            'parent sleep',
            'cancel start',
            'child slept',
            'child cancelled',
            'cancel done'
            ]


def test_double_cancel(kernel):
    results = []

    async def sleeper():
        results.append('start')
        try:
            await sleep(1)
            results.append('not here')
        except CancelledError:
            results.append('cancel request')
            await sleep(1)
            results.append('cancelled')

    async def main():
        task = await spawn(sleeper())
        await sleep(0.5)
        try:
            await timeout_after(1, task.cancel())
        except TaskTimeout:
            results.append('retry')
            await task.cancel()    # This second cancel should not abort any operation in sleeper
            results.append('done cancel')

    kernel.run(main())
    assert results == [
            'start',
            'cancel request',
            'retry',
            'cancelled',
            'done cancel'
            ]

