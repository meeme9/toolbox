# -*- coding: utf-8 -*-
import os
import sys

from .processor import Processor


class ProcessorFunc(Processor):
    def __init__(self, logger, task_dir, step, func, config):
        super(ProcessorFunc, self).__init__(logger, task_dir, step)
        logger.info("init odps download")
        self.func = func
        self.config = config

    def process(self, input_files):
        return self.func(self.logger, self.process_dir, input_files, self.config)