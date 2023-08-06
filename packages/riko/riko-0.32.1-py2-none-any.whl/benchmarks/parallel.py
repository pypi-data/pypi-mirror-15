from __future__ import absolute_import, division, print_function, with_statement

from os import path as p
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool
from time import time, sleep

from builtins import *

from riko.collections.sync import (
    SyncPipe, SyncCollection, get_chunksize, get_worker_cnt)

from riko.bado import coroutine, return_value, react
from riko.collections.async import AsyncPipe, AsyncCollection
from riko.bado.util import asyncSleep
from riko.bado.itertools import asyncImap
from riko.modules.pipefetch import pipe, asyncPipe

NUMBER = 3
LOOPS = 3
DELAY = 0.2

parent = p.join(p.abspath(p.dirname(p.dirname(__file__))), 'data')
files = [
    'ouseful.xml',
    'feed.xml',
    'delicious.xml',
    'psychemedia.xml',
    'ouseful_feedburner.xml',
    'TheEdTechie.xml',
    'yodel.xml',
    'gawker.xml',
    'health.xml',
    'topstories.xml',
    'autoblog.xml',
    'fourtitude.xml',
    'greenhughes.xml',
    'psychemedia_slideshare.xml']

get_path = lambda name: 'file://%s' % p.join(parent, name)
sources = [{'url': get_path(f)} for f in files]
length = len(files)
conf = {'url': [{'value': get_path(f)} for f in files], 'sleep': DELAY}
iterable = [DELAY for x in files]


def baseline_sync():
    return map(sleep, iterable)


def baseline_threads():
    workers = get_worker_cnt(length)
    chunksize = get_chunksize(length, workers)
    pool = ThreadPool(workers)
    return list(pool.imap_unordered(sleep, iterable, chunksize=chunksize))


def baseline_procs():
    workers = get_worker_cnt(length, False)
    chunksize = get_chunksize(length, workers)
    pool = Pool(workers)
    return list(pool.imap_unordered(sleep, iterable, chunksize=chunksize))


def sync_pipeline():
    return list(pipe(conf=conf))


def sync_pipe():
    return SyncPipe('fetch', conf=conf).list


def sync_collection():
    return SyncCollection(sources, sleep=DELAY).list


def par_sync_collection():
    return SyncCollection(sources, parallel=True, sleep=DELAY).list


def baseline_async():
    return asyncImap(asyncSleep, iterable)


def async_pipeline():
    d = asyncPipe(conf=conf)
    d.addCallbacks(list, print)
    return d


def async_pipe():
    return AsyncPipe('fetch', conf=conf).list


def async_collection():
    return AsyncCollection(sources, sleep=DELAY).list


def parse_results(results):
    switch = {0: 'secs', 3: 'msecs', 6: 'usecs'}
    best = min(results)

    for places in [0, 3, 6]:
        factor = pow(10, places)
        if 1 / best // factor == 0:
            break

    return round(best * factor, 2), switch[places]


def print_time(test, max_chars, run_time, units):
    padded = test.zfill(max_chars).replace('0', ' ')
    msg = '%s - %i repetitions/loop, best of %i loops: %s %s'
    print(msg % (padded, NUMBER, LOOPS, run_time, units))


@coroutine
def run_async(reactor, tests, max_chars):
    for test in tests:
        results = []

        for i in range(LOOPS):
            loop = 0

            for j in range(NUMBER):
                start = time()
                yield test()
                loop += time() - start

            results.append(loop)

        run_time, units = parse_results(results)
        print_time(test.func_name, max_chars, run_time, units)

    return_value(None)

if __name__ == '__main__':
    from timeit import repeat

    run = partial(repeat, repeat=LOOPS, number=NUMBER)
    sync_tests = [
        'baseline_sync', 'baseline_threads', 'baseline_procs', 'sync_pipeline',
        'sync_pipe', 'sync_collection', 'par_sync_collection']

    async_tests = [baseline_async, async_pipeline, async_pipe, async_collection]
    combined_tests = sync_tests + [f.func_name for f in async_tests]
    max_chars = max(map(len, combined_tests))

    for test in sync_tests:
        results = run('%s()' % test, setup='from __main__ import %s' % test)
        run_time, units = parse_results(results)
        print_time(test, max_chars, run_time, units)

    react(run_async, [async_tests, max_chars])
