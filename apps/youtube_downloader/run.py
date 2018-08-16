# -*- coding: utf-8 -*-
import argparse
import logging
import base64
from lib.process import *
from lib.tools.web_utils import *


def get_url_list(logger, process_dir, input_files, config):
    postdata = {
        'ctl00$ContentPlaceHolder1$txtPlaylist': config['list_id'],
        'ctl00$ContentPlaceHolder1$btnSubmit': 'Submit',
        '__VIEWSTATEGENERATOR': '0A525D99',
        '__VIEWSTATE': '/wEPDwUJMjA1NTc2NjUyD2QWAmYPZBYCAgEPZBYCAhMPFQEgL2phdmFzY3JpcHQvanF1ZXJ5LTEuMTAuMi5taW4uanNkZLmpyenldSJnY/JJOXOWPT0NkHq0',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': ''
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1; rv:20.0) Gecko/20100101 Firefox/20.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Cache-Control': 'max-age=0',
        'Accept-Encoding' : 'gzip, deflate',
        'Connection' : 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': '__utma=261291275.1251789180.1534345575.1534345575.1534345575.1; __utmc=261291275; __utmz=261291275.1534345575.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',

        'Host': 'www.williamsportwebdeveloper.com',
        'Origin': 'http://www.williamsportwebdeveloper.com',
        'Referer': 'http://www.williamsportwebdeveloper.com/FavBackUp.aspx'
    }

    import requests
    s = requests.Session()
    q = s.post('http://www.williamsportwebdeveloper.com/FavBackUp.aspx', headers=headers, data=postdata)

    output_file = os.path.join(process_dir, '1.html')

    with open(output_file, 'wb') as outf:
        outf.write(q.content)

    return [output_file]


def download_list(logger, process_dir, input_files, config):
    return_file_list = []

    from lxml import html
    root = html.fragment_fromstring('<html>' + open(input_files[0]).read() + '</html>')

    index = 0
    for el in root.xpath("//table/tr"):
        childs = [child for child in el if child.tag == 'td']
        if len(childs) == 5 and index != 0:
            url = childs[1].text_content()
            file_name = childs[3].text_content().split('|')[0].strip() + '.mp4'
            logger.info('downloading: {}, {}'.format(url, file_name))
            find_url = 'http://www.findyoutube.com/parse.php?url=' + base64.b64encode(bytearray(str(url), encoding='utf-8')).decode('utf-8') #  aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj14UUplSVB6RzltUQ==
            page = get_page(find_url)
            download_urls = [x for x in enum_html_path(page, "//a[text()='MP4-1280*720']/@href")]
            logger.info(download_urls[0])
            wget_download_file(download_urls[0], process_dir, file_name)
            return_file_list.append(os.path.join(process_dir, file_name))
            logger.info('success:{}'.format(file_name))
        elif len(childs) == 5:
            index += 1
    return return_file_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download url')
    parser.add_argument('--dir', required=True)
    parser.add_argument('--url', required=True)
    parser.add_argument('--type', type=str, default='url',choices=['url', 'list'])
    args = parser.parse_args()
    print(args.dir)
    print(args.url)
    print(args.type)

    config = {
        'task_dir': args.dir,
        'type': 'list',
        'list_id': args.url  # 'UUx1xhxQyzR4TT6PmXO0khbQ'
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
    proc = ProcessorFunc(logger, config['task_dir'], step_str, get_url_list, config)
    file_list = proc.run([])

    # step 1
    step += 1
    step_str = "step_" + str(step)
    proc = ProcessorFunc(logger, config['task_dir'], step_str, download_list, config)
    file_list = proc.run(file_list)
