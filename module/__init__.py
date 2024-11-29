# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/11/18 12:28:18
# File:__init__.py
import os
import sys
import yaml
import atexit
import readline
import datetime
import mimetypes
from ctypes import windll
from loguru import logger
from pyrogram import utils
from rich.console import Console
from rich.markdown import Markdown
from typing import Tuple, List, Dict, Any, Optional


def print_helper():
    config_helper = r"""
# 配置文件说明
```yaml
# 下载完成直接打开软件即可,软件会一步一步引导你输入的!这里只是介绍每个参数的含义
# 填入第一步教你申请的api_hash和api_id
# 如果是按照软件的提示填,不需要加引号,如果是手动打开config.yaml修改配置,请仔细阅读下面内容
# 手动填写注意区分冒号类型,例如 - 是:不是：
# 手动填写的时候还请注意参数冒号不加空格会报错 后面有一个空格,例如 - api_hash: xxx而不是api_hash:xxx
api_hash: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #api_hash没有引号
api_id: 'xxxxxxxx' #注意配置文件中只有api_id有引号！！！
links: D:\path\where\your\link\txt\save\content.txt # 链接地址写法如下:
# 新建txt文本,一个链接为一行,将路径填入即可请不要加引号,在软件运行前就准备好
# D:\path\where\your\link\txt\save\content.txt 请注意一个链接一行
# 列表写法已在v1.1.0版本中弃用,目前只有上述唯一写法！！！
# 不要存在中文或特殊字符
max_download_task: 3 # 最大的同时下载任务数 注意:如果你不是Telegram会员,那么最大同时下载数只有1
proxy: # 代理部分,如不使用请全部填null注意冒号后面有空格,否则不生效导致报错!
  enable_proxy: true # 是否开启代理 true为开启 false为关闭
  hostname: 127.0.0.1 # 代理的ip地址
  is_notice: false # 是否开启代理提示, true为每次打开询问你是否开启代理, false则为关闭
  scheme: socks5 # 代理的类型,支持http,socks4,socks5
  port: 10808 # 代理ip的端口
  username: null # 代理的账号,有就填,没有请都填null!
  password: null # 代理的密码,有就填,没有请都填null!
save_path: F:\path\the\media\where\you\save # 下载的媒体保存的地址,没有引号,不要存在中文或特殊字符
# 再次提醒,由于nuitka打包的性质决定,中文路径无法被打包好的二进制文件识别,故在配置文件时无论是链接路径还是媒体保存路径都请使用英文命名。
is_shutdown: true # 是否下载完成后自动关机 true为下载完成后自动关机 false为下载完成后不关机
```
"""
    markdown = Markdown(config_helper)
    console.print(markdown)


# v1.1.2 解决链接若附带/c字段即私密频道无法下载的问题,是由于pyrogram的问题:https://github.com/pyrogram/pyrogram/issues/1314
def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


def read_input_history(history_path: str, max_record_len: int):
    # 尝试读取历史记录文件
    try:
        readline.read_history_file(history_path)
    except FileNotFoundError:
        pass
    # 设置历史记录的最大长度
    readline.set_history_length(max_record_len)
    # 注册退出时保存历史记录
    atexit.register(readline.write_history_file, history_path)


def check_run_env():  # 检测是控制台运行还是IDE运行
    return windll.kernel32.SetConsoleTextAttribute(windll.kernel32.GetStdHandle(-0xb), 0x7)


# 自定义 yaml文件中 None 的表示
class CustomDumper(yaml.Dumper):
    def represent_none(self, data):
        return self.represent_scalar('tag:yaml.org,2002:null', '~')


console = Console()
utils.get_peer_type = get_peer_type_new
__version__ = '1.1.7'
__license__ = "MIT License"
__copyright__ = "Copyright (C) 2024 Gentlesprite <https://github.com/Gentlesprite>"
__update_date__ = '2024/11/29 12:29:43'
SOFTWARE_FULL_NAME = 'Telegram Restricted Media Downloader'
SOFTWARE_NAME = 'TRMD'
author = 'Gentlesprite'
APPDATA_PATH = os.path.join(os.environ['APPDATA'], SOFTWARE_NAME)
LOG_PATH = os.path.join(APPDATA_PATH, f'{SOFTWARE_NAME}_LOG.log')
INPUT_HISTORY_PATH = os.path.join(APPDATA_PATH, f'.{SOFTWARE_NAME}_HISTORY')
MAX_RECORD_LENGTH = 1000
read_input_history(history_path=INPUT_HISTORY_PATH, max_record_len=MAX_RECORD_LENGTH)
# 配置日志输出到文件
logger.add(sink=LOG_PATH, level='INFO', rotation='10 MB', retention='10 days', compression='zip', encoding='UTF-8',
           enqueue=True)
CustomDumper.add_representer(type(None), CustomDumper.represent_none)
print_helper()
