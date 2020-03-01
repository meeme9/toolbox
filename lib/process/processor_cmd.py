# -*- coding: utf-8 -*-
import os
import sys

from .processor import Processor


class ProcessorCMD(Processor):
    def __init__(self, logger, task_dir, step, cmd):
        super().__init__(logger, task_dir, step)
        logger.info("init odps download")
        self.cmd = cmd

    def process(self, input_files):
        self.logger.info("running cmd: {}".format(self.cmd))
        sys.stdout.flush()
        ret_value = os.system(self.cmd)
        if ret_value != 0:
            raise RuntimeError('cmd error')
        return [os.path.join(self.process_dir, f) for f in os.listdir(self.process_dir)]
