import random
import logging
import threading

from esrally import time
from esrally.track import track
from esrally.utils import convert, progress

logger = logging.getLogger("rally.driver")


class Driver:
    BENCHMARKS = {
        track.BenchmarkPhase.search: lambda: SearchBenchmark,
        track.BenchmarkPhase.stats: lambda: StatsBenchmark,
        track.BenchmarkPhase.index: lambda: ThreadedIndexBenchmark
    }

    """
    Driver runs the benchmark.
    """

    def __init__(self, config, cluster, track, track_setup, clock=time.Clock):
        self.cfg = config
        self.cluster = cluster
        self.track = track
        self.track_setup = track_setup
        self.clock = clock

    def go(self):
        self.cluster.on_benchmark_start()
        # We need to run phases in order - i.e. indexing has to be done before a search can be started
        for phase in track.BenchmarkPhase:
            if phase in self.track_setup.benchmark:
                self._run(Driver.BENCHMARKS[phase]())
        self.cluster.on_benchmark_stop()

    def _run(self, benchmark_class):
        benchmark = benchmark_class(self.cfg, self.clock, self.track, self.track_setup, self.cluster)
        phase = benchmark.phase
        logger.info("Starting %s benchmark for track [%s] and track setup [%s]" % (phase.name, self.track.name, self.track_setup.name))
        self.cluster.on_benchmark_start(phase)
        benchmark.run()
        self.cluster.on_benchmark_stop(phase)
        logger.info("Stopped %s benchmark for track [%s] and track setup [%s]" % (phase.name, self.track.name, self.track_setup.name))


class Benchmark:
    def __init__(self, cfg, clock, track, track_setup, cluster, phase):
        self.cfg = cfg
        self.clock = clock
        self.track = track
        self.track_setup = track_setup
        self.cluster = cluster
        self.phase = phase
        self.metrics_store = cluster.metrics_store
        self.progress = progress.CmdLineProgressReporter()
        self.quiet_mode = self.cfg.opts("system", "quiet.mode")


class LatencyBenchmark(Benchmark):
    def __init__(self, cfg, clock, track, track_setup, cluster, phase, queries, repetitions=1000):
        Benchmark.__init__(self, cfg, clock, track, track_setup, cluster, phase)
        self.queries = queries
        self.repetitions = repetitions
        self.stop_watch = self.clock.stop_watch()

    def run(self):
        logger.info("Running warmup iterations")
        self._run_benchmark("  Benchmarking %s (warmup iteration %d/%d)")
        logger.info("Running measurement iterations")
        times = self._run_benchmark("  Benchmarking %s (iteration %d/%d)")

        for q in self.queries:
            latencies = [t[q.name] for t in times]
            for latency in latencies:
                self.metrics_store.put_value_cluster_level("query_latency_%s" % q.name, convert.seconds_to_ms(latency), "ms")

    def _run_benchmark(self, message):
        times = []
        quiet = self.quiet_mode
        if not quiet:
            self._print_progress(message, 0)
        for iteration in range(1, self.repetitions + 1):
            if not quiet:
                self._print_progress(message, iteration)
            times.append(self._run_one_round())
        self.progress.finish()
        return times

    def _print_progress(self, message, iteration):
        if iteration % (self.repetitions // 20) == 0:
            progress_percent = round(100 * iteration / self.repetitions)
            self.progress.print(message % (self.phase.name, iteration, self.repetitions), "[%3d%% done]" % progress_percent)

    def _run_one_round(self):
        d = {}
        es = self.cluster.client
        for query in self.queries:
            self.stop_watch.start()
            query.run(es)
            self.stop_watch.stop()
            d[query.name] = self.stop_watch.total_time() / query.normalization_factor
            query.close(es)
        return d


class SearchBenchmark(LatencyBenchmark):
    def __init__(self, cfg, clock, t, track_setup, cluster):
        super().__init__(cfg, clock, t, track_setup, cluster, track.BenchmarkPhase.search, t.queries,
                         track_setup.benchmark[track.BenchmarkPhase.search].iteration_count)


class StatsQueryAdapter:
    def __init__(self, name, op, *args, **kwargs):
        self.name = name
        self.op = op
        self.args = args
        self.kwargs = kwargs
        self.normalization_factor = 1

    def run(self, client):
        self.op(*self.args, **self.kwargs)

    def close(self, client):
        pass

    def __str__(self):
        return self.name


class StatsBenchmark(LatencyBenchmark):
    def __init__(self, cfg, clock, t, track_setup, cluster):
        super().__init__(cfg, clock, t, track_setup, cluster, track.BenchmarkPhase.stats, [
            StatsQueryAdapter("indices_stats", cluster.indices_stats, metric="_all", level="shards"),
            StatsQueryAdapter("node_stats", cluster.nodes_stats, metric="_all", level="shards"),
        ], track_setup.benchmark[track.BenchmarkPhase.stats].iteration_count)


class IndexedDocumentCountProbe:
    def __init__(self, cluster, expected_doc_count):
        self.cluster = cluster
        self.expected_doc_count = expected_doc_count

    def assert_doc_count(self):
        stats = self.cluster.indices_stats(metric="_all", level="shards")
        actual_doc_count = stats["_all"]["primaries"]["docs"]["count"]
        if self.expected_doc_count is not None and self.expected_doc_count != actual_doc_count:
            msg = "Wrong number of documents indexed: expected %s but got %s. If you benchmark against an external cluster be sure to " \
                  "start with all indices empty." % (self.expected_doc_count, actual_doc_count)
            logger.error(msg)
            raise AssertionError(msg)


class IndexBenchmark(Benchmark):
    def __init__(self, cfg, clock, t, track_setup, cluster):
        Benchmark.__init__(self, cfg, clock, t, track_setup, cluster, track.BenchmarkPhase.index)
        self.stop_watch = clock.stop_watch()
        self.bulk_size = track_setup.benchmark[track.BenchmarkPhase.index].bulk_size
        self.processed = 0

    def run(self):
        logger.info("Use %d docs per bulk request" % self.bulk_size)
        finished = False
        try:
            self.index()
            finished = True
        finally:
            self.progress.finish()
            logger.info("IndexBenchmark finished successfully: %s" % finished)

    def index(self):
        force_merge = self.track_setup.benchmark[self.phase].force_merge
        docs_to_index = self.track.number_of_documents

        conflicts = self.track_setup.benchmark[self.phase].id_conflicts
        if conflicts == track.IndexIdConflict.NoConflicts:
            doc_count_probe = IndexedDocumentCountProbe(self.cluster, docs_to_index)
            ids = None
        else:
            # We cannot know how many docs have been updated if we produce id conflicts
            doc_count_probe = IndexedDocumentCountProbe(self.cluster, None)
            ids = self.build_conflicting_ids(conflicts)

        self.index_documents(ids)

        self.cluster.force_flush()
        if force_merge:
            self.cluster.force_merge()

        doc_count_probe.assert_doc_count()

    def build_conflicting_ids(self, conflicts):
        docs_to_index = self.track.number_of_documents
        logger.info('build ids with id conflicts of type %s' % conflicts)

        all_ids = [0] * docs_to_index
        for i in range(docs_to_index):
            if conflicts == track.IndexIdConflict.SequentialConflicts:
                all_ids[i] = '%10d' % i
            elif conflicts == track.IndexIdConflict.RandomConflicts:
                all_ids[i] = '%10d' % random.randint(0, docs_to_index)
            else:
                raise RuntimeError('Unknown id conflict type %s' % conflicts)
        return all_ids

    def _print_progress(self, docs_processed):
        if not self.quiet_mode:
            # stack-confine asap to keep the reporting error low (this number may be updated by other threads), we don't need to be entirely
            # accurate here as this is "just" a progress report for the user
            docs_total = self.track.number_of_documents
            elapsed = self.stop_watch.split_time()
            docs_per_second = docs_processed / elapsed
            self.progress.print(
                "  Benchmarking indexing at %.1f docs/s" % docs_per_second,
                "[%3d%% done]" % round(100 * docs_processed / docs_total)
            )
            logger.info("Indexer: %d docs: [%.1f docs/s]" % (docs_processed, docs_per_second))

    def index_documents(self, ids):
        raise NotImplementedError("abstract method")


class ThreadedIndexBenchmark(IndexBenchmark):
    def __init__(self, config, clock, track, track_setup, cluster):
        super().__init__(config, clock, track, track_setup, cluster)

    def index_documents(self, ids):
        num_client_threads = int(self.cfg.opts("benchmarks", "index.clients"))
        logger.info("Launching %d client bulk indexing threads" % num_client_threads)

        self.stop_watch.start()
        self._print_progress(self.processed)

        for index in self.track.indices:
            for type in index.types:
                if type.document_file_name:
                    documents = self.cfg.opts("benchmarks", "dataset.path")
                    docs_file = documents[type]
                    logger.info("Indexing JSON docs file: [%s]" % docs_file)

                    start_signal = CountDownLatch(1)
                    stop_event = threading.Event()
                    failed_event = threading.Event()
                    docs_to_index = self.track.number_of_documents

                    iterator = BulkIterator(index.name, type.name, docs_file, ids, docs_to_index, self.bulk_size)

                    threads = []
                    try:
                        for i in range(num_client_threads):
                            t = threading.Thread(target=self.bulk_index, args=(start_signal, iterator, failed_event, stop_event))
                            t.setDaemon(True)
                            t.start()
                            threads.append(t)

                        start_signal.count_down()
                        for t in threads:
                            t.join()

                    except KeyboardInterrupt:
                        stop_event.set()
                        for t in threads:
                            t.join()

                    if failed_event.isSet():
                        raise RuntimeError("some indexing threads failed")

        self.stop_watch.stop()
        self._print_progress(self.processed)
        docs_per_sec = (self.processed / self.stop_watch.total_time())
        self.metrics_store.put_value_cluster_level("indexing_throughput", round(docs_per_sec), "docs/s")

    def bulk_index(self, start_signal, bulk_iterator, failed_event, stop_event):
        """
        Runs one (client) bulk index thread.
        """
        start_signal.await()

        while not stop_event.isSet():
            buffer, document_count = bulk_iterator.next_bulk()
            if document_count == 0:
                break
            data = "\n".join(buffer)
            del buffer[:]

            try:
                self.cluster.client.bulk(body=data, params={'request_timeout': 60000})
            except BaseException as e:
                logger.error("Indexing failed: %s" % e)
                failed_event.set()
                stop_event.set()
                raise
            self.update_bulk_status(document_count)

    def update_bulk_status(self, count):
        self.processed += count
        if self.processed % 10000 == 0:

            self._print_progress(self.processed)
            # use 10% of all documents for warmup before gathering metrics
            if self.processed > self.track.number_of_documents / 10:
                elapsed = self.stop_watch.split_time()
                docs_per_sec = (self.processed / elapsed)
                self.metrics_store.put_value_cluster_level("indexing_throughput", round(docs_per_sec), "docs/s")


class CountDownLatch:
    def __init__(self, count=1):
        self.count = count
        self.lock = threading.Condition()

    def count_down(self):
        with self.lock:
            self.count -= 1

            if self.count <= 0:
                self.lock.notifyAll()

    def await(self):
        with self.lock:
            while self.count > 0:
                self.lock.wait()


class BulkIterator:
    def __init__(self, index_name, type_name, documents, ids, docs_to_index, bulk_size):
        self.f = open(documents, 'rt')
        self.index_name = index_name
        self.type_name = type_name
        self.current_bulk = 0
        self.id_up_to = 0
        self.ids = ids
        self.file_lock = threading.Lock()
        self.docs_to_index = docs_to_index
        self.rand = random.Random(17)
        self.bulk_size = bulk_size
        self.indexed_document_count = 0

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    def next_bulk(self):

        """
        Returns lines for one bulk request.
        """

        buffer = []
        try:
            with self.file_lock:
                docs_left = self.docs_to_index - (self.current_bulk * self.bulk_size)
                if self.f is None or docs_left <= 0:
                    return [], 0

                self.current_bulk += 1
                limit = 2 * min(self.bulk_size, docs_left)

                while True:
                    line = self.f.readline()
                    if len(line) == 0:
                        self.close()
                        break
                    line = line.strip()

                    if self.ids is not None:
                        # 25% of the time we replace a doc:
                        if self.id_up_to > 0 and self.rand.randint(0, 3) == 3:
                            id = self.ids[self.rand.randint(0, self.id_up_to - 1)]
                        else:
                            id = self.ids[self.id_up_to]
                            self.id_up_to += 1
                        cmd = '{"index": {"_index": "%s", "_type": "%s", "_id": "%s"}}' % (self.index_name, self.type_name, id)
                    else:
                        cmd = '{"index": {"_index": "%s", "_type": "%s"}}' % (self.index_name, self.type_name)

                    buffer.append(cmd)
                    buffer.append(line)

                    if len(buffer) >= limit:
                        break

            # contains index commands and data (in bulk format), hence 2 lines per record
            document_count = len(buffer) / 2
            self.indexed_document_count += document_count
            return buffer, document_count
        except BaseException as e:
            logger.exception("Could not read")
