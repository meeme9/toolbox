# -*- coding: utf-8 -*-
import os
import sys
import itertools
from multiprocessing import Pool

from .processor import Processor


class ProcessorParallel(Processor):
    def __init__(self, logger, task_dir, step, func, process_num=4):
        super(ProcessorParallel, self).__init__(logger, task_dir, step)
        self.func = func
        self.pool = Pool(processes=process_num)  # start 4 worker processes

    def process(self, input_files):
        results = p.map(self.func, input_files)
        return list(itertools.chain.from_iterable(results))
