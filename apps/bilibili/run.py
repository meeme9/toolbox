# -*- coding: utf-8 -*-
import argparse
import logging
from lib.process import *
from lib.tools.web_utils import *


def bilibili_download(logger, process_dir, input_files, config):
    cmd = "you-get -l "
    if config["format"] is not None:
        cmd += "--format=" + config["format"] + " "
    cmd += "-o " + process_dir + " "
    cmd += config['url']

    ret_value = os.system(cmd)
    if ret_value != 0:
        raise RuntimeError('cmd error')

    file_list = [os.path.join(process_dir, f) for f in os.listdir(process_dir) if f.endswith('.flv')]
    mp4_file_list = []
    for file in file_list:
        new_file = file.replace('.flv', '.mp4')
        os.system(f"ffmpeg -i '{file}' '{new_file}'")
        mp4_file_list.append(new_file)

    return mp4_file_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download url')
    parser.add_argument('--dir', required=True)
    parser.add_argument('--url', required=True)
    parser.add_argument('--format', required=False)
    # parser.add_argument('--type', type=str, default='url',choices=['url', 'list'])
    args = parser.parse_args()
    print(args.dir)
    print(args.url)
    print(args.format)

    config = {
        'task_dir': args.dir,
        'format': args.format,
        'url': args.url
    }

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s %(message)s',
        datefmt='[%Y-%m-%d %H:%M:%S]',
        filename=os.path.join(config['task_dir'], "1.log"))
    logger = logging.getLogger("Service")

    # step 0
    step = 0
    step_str = "step_" + str(step)
    proc = ProcessorFunc(logger, config['task_dir'], step_str, bilibili_download, config)
    file_list = proc.run([])