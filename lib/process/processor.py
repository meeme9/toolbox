# -*- coding: utf-8 -*-
import json
import os


class Processor:
    def __init__(self, logger, task_dir, step):
        self.logger = logger
        self.task_dir = task_dir
        self.step = step
        self.process_dir = os.path.join(task_dir, step)
        if not os.path.exists(self.process_dir):
            os.makedirs(self.process_dir)

    def run(self, input_files):
        done_file = os.path.join(self.task_dir, self.step + ".done")
        if os.path.exists(done_file):
            with open(done_file) as fp:
                file_list = json.load(fp)
                return file_list
        else:
            file_list = self.process(input_files)
            with open(done_file, "w") as fp:
                fp.write(json.dumps(file_list))
                fp.flush()
            return file_list

    def process(self, input_files):
        raise NotImplementedError()
