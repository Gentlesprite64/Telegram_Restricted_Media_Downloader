# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2025/2/27 17:38
# File:task.py
from functools import wraps

from module import console, log
from module.enums import DownloadStatus, LinkType, KeyWord, Status


class Task:
    LINK_INFO: dict = {}
    COMPLETE_LINK: set = set()

    def __init__(self,
                 link: str,
                 link_type: str or None,
                 member_num: int,
                 complete_num: int,
                 file_name: set,
                 error_msg: dict):
        Task.LINK_INFO[link] = {
            'link_type': link_type,
            'member_num': member_num,
            'complete_num': complete_num,
            'file_name': file_name,
            'error_msg': error_msg
        }

    def on_create_task(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            link = kwargs.get('link')
            Task(link=link, link_type=None, member_num=0, complete_num=0, file_name=set(), error_msg={})
            res: dict = await func(self, *args, **kwargs)
            chat_id, link_type, member_num, status, e_code = res.values()
            if status == DownloadStatus.FAILURE:
                Task.LINK_INFO.get(link)['error_msg'] = e_code
                reason: str = e_code.get('all_member')
                if reason:
                    log.error(f'{KeyWord.LINK}:"{link}"{e_code.get('error_msg')},'
                              f'{KeyWord.REASON}:"{reason},"'
                              f'{KeyWord.STATUS}:{Status.FAILURE}。')
                else:
                    log.warning(
                        f'{KeyWord.LINK}:"{link}"{e_code.get('error_msg')},'
                        f'{KeyWord.STATUS}:{Status.FAILURE}。')
            elif status == DownloadStatus.DOWNLOADING:
                Task.LINK_INFO.get(link)['link_type'] = link_type
                Task.LINK_INFO.get(link)['member_num'] = member_num
                console.log(
                    f'{KeyWord.CHANNEL}:"{chat_id}",'  # 频道名。
                    f'{KeyWord.LINK}:"{link}",'  # 链接。
                    f'{KeyWord.LINK_TYPE}:{LinkType.t(link_type)}。')  # 链接类型。
            return res

        return wrapper

    def on_complete(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            link, file_name = res
            Task.LINK_INFO.get(link).get('file_name').add(file_name)
            for i in Task.LINK_INFO.items():
                compare_link: str = i[0]
                info: dict = i[1]
                if compare_link == link:
                    info['complete_num'] = len(info.get('file_name'))
            all_num: int = Task.LINK_INFO.get(link).get('member_num')
            complete_num: int = Task.LINK_INFO.get(link).get('complete_num')
            if all_num == complete_num:
                console.log(f'{KeyWord.LINK}:"{link}",'
                            f'{KeyWord.STATUS}:{Status.SUCCESS}。')
                Task.LINK_INFO.get(link)['error_msg'] = {}
                Task.COMPLETE_LINK.add(link)
            return res

        return wrapper
