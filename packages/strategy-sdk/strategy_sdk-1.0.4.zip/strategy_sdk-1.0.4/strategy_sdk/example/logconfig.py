# encoding: utf-8

__author__ = 'fzh89'

# vim : set expandtab ts=4 sw=4 sts=4 tw=100 :

import logging
from logging.handlers import TimedRotatingFileHandler


def configure_log(filename):
    # 日志打印格式
    log_fmt = '%(asctime)s\t%(filename)s,line %(lineno)s\t%(levelname)s: %(message)s'
    formatter = logging.Formatter(log_fmt)
    # 创建TimedRotatingFileHandler对象
    log_file_handler = TimedRotatingFileHandler(filename=filename, when="D", interval=1, backupCount=12)
    log_file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO,
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filemode='a')
    log = logging.getLogger()
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # 设置日志打印格式
    formatter = logging.Formatter(log_fmt)
    console.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    log.addHandler(console)
    log.addHandler(log_file_handler)
    return log


if __name__ == "__main__":
    configure_log()
