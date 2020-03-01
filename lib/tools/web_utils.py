# -*- coding: utf-8 -*-
import socks
import socket
import urllib.request as request
from lxml import html
import gzip
import os


def get_page(url, charset="utf-8", timeout=100, use_proxy=True, retries=5):
    bak_socket = None
    if use_proxy:
        bak_socket = socket.socket
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
        socket.socket = socks.socksocket

    retry = 0
    while retry < retries:
        try:
            req = request.Request(url)

            with request.urlopen(req, timeout=timeout) as response:
                if response.getheader("Content-Encoding") == "gzip":
                    tmp = gzip.decompress(response.read()).decode(charset)
                else:
                    tmp = response.read().decode(charset)
                if use_proxy:
                    request.install_opener(None)
                return tmp
        except Exception as expt:
            print("error occurs when crawling url %s, error= %s" % (url, str(expt)))
            retry += 1

    if use_proxy:
        socket.socket = bak_socket
    raise IOError('get page error')


def download_file(url, process_dir, file_name, overwrite=False, retries=3):
    if not overwrite and os.path.exists(os.path.join(process_dir, file_name)):
        return
    retry = 0
    while retry < retries:
        try:
            local_tmp_file = os.path.join(process_dir, '_.tmp')
            if os.path.exists(local_tmp_file):
                os.remove(local_tmp_file)
            request.urlretrieve(url, local_tmp_file)
            os.rename(local_tmp_file, os.path.join(process_dir, file_name))
            return True
        except Exception as expt:
            print(
                "error occurs when downloading %s to %s, retry = %d, error = %s" % (url, file_name, retry, str(expt)))
            retry += 1
    raise IOError('download failed')


def wget_download_file(url, process_dir, file_name, use_proxy=False, overwrite=False, retries=3):
    if not overwrite and os.path.exists(os.path.join(process_dir, file_name)):
        return
    retry = 0
    while retry < retries:
        try:
            local_tmp_file = os.path.join(process_dir, '_.tmp')
            if os.path.exists(local_tmp_file):
                os.remove(local_tmp_file)
            if use_proxy:
                os.system("tsocks wget -O {} '{}'".format(local_tmp_file, url))
            else:
                os.system("wget -O {} '{}'".format(local_tmp_file, url))
            os.rename(local_tmp_file, os.path.join(process_dir, file_name))
            return True
        except Exception as expt:
            print(
                "error occurs when downloading %s to %s, retry = %d, error = %s" % (url, file_name, retry, str(expt)))
            retry += 1
    raise IOError('wget download failed')


def enum_html_path(content, xpath):
    root = html.fromstring(content)
    for el in root.xpath(xpath):
        yield str(el)


if __name__ == '__main__':
    ss = get_page('http://www.findyoutube.com/parse.php?url=aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj14UUplSVB6RzltUQ==', charset="utf-8")
    for x in enum_html_path(ss, "//a[text()='MP4-1280*720']/@href"):
        print(x)
