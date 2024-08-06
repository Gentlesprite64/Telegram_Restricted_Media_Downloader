# coding=UTF-8
# Author:LZY/我不是盘神
# Software:PyCharm
# Time:2023/10/3 1:00:03
# File:break_download_limit.py
import os
import shutil
import asyncio
import pyrogram
from typing import List, Any
from module.pyrogram_extension import get_extension
from module.process_path import split_path, is_folder_empty, is_exist, validate_title, truncate_filename
from module.enum_define import LinkType, DownloadStatus, KeyWorld, LogLevel
from module.unit import suitable_units_display
from module.meta import print_meta
from module.logger_config import print_with_log

downloading = DownloadStatus.downloading.text
success_download = DownloadStatus.success.text
failure_download = DownloadStatus.failure.text
skip_download = DownloadStatus.skip.text
all_complete = DownloadStatus.all_complete.text
keyword_link = KeyWorld.link.text
keyword_link_type = KeyWorld.link_type.text
keyword_id = KeyWorld.id.text
keyword_size = KeyWorld.size.text
keyword_link_status = KeyWorld.status.text
keyword_file = KeyWorld.file.text
keyword_error_size = KeyWorld.error_size.text
keyword_actual_size = KeyWorld.actual_size.text
keyword_already_exist = KeyWorld.already_exist.text
keyword_reading = KeyWorld.reading.text
keyword_label = KeyWorld.label.text


def _move_to_download_path(temp_save_path: str, save_path: str):
    os.makedirs(save_path, exist_ok=True)
    if os.path.isdir(save_path):
        shutil.move(temp_save_path, save_path)
    else:
        print_with_log(msg=f'"{save_path}"不是一个目录,已将文件下载到默认目录。', level=LogLevel.error)
        if is_folder_empty(save_path):
            os.rmdir(save_path)
        save_path = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(save_path, exist_ok=True)
        shutil.move(temp_save_path, save_path)


def _get_temp_path(message: pyrogram.types.Message,
                   media_obj: str,
                   temp_folder: str) -> str:
    file_name = None
    os.makedirs(temp_folder, exist_ok=True)
    if media_obj == 'video':
        file_name = "{} - {}.{}".format(
            message.id,
            os.path.splitext(f'{message.video.file_name}')[0],
            get_extension(file_id=message.video.file_id, mime_type='video', dot=False)
        )
        file_name = os.path.join(temp_folder, validate_title(file_name))
    elif media_obj == 'photo':
        file_name = "{} - {}.{}".format(
            message.id,
            message.photo.file_unique_id,
            get_extension(file_id=message.photo.file_id, mime_type='photo', dot=False)
        )
        file_name = os.path.join(temp_folder, validate_title(file_name))
    return truncate_filename(file_name)


def _check_download_finish(sever_size: Any, download_path: Any, save_directory):
    if isinstance(sever_size, dict) and isinstance(download_path, list):  # 组
        local_size_dict: dict = {}
        for name in download_path:
            size = os.path.getsize(name)
            local_size_dict[name] = size
        for temp_save_path, sever_size in zip(download_path, sever_size.values()):
            local_size = os.path.getsize(temp_save_path)
            format_local_size, format_sever_size = suitable_units_display(local_size), suitable_units_display(
                sever_size)
            save_path = os.path.join(save_directory, split_path(temp_save_path)[1])
            if local_size == sever_size:
                _move_to_download_path(temp_save_path=temp_save_path, save_path=save_directory)
                print_with_log(
                    msg=f'{keyword_file}:"{save_path}",{keyword_size}:{format_local_size},{keyword_link_status}:{DownloadStatus.success.text}。',
                    level=LogLevel.success)
            else:
                print_with_log(msg=
                               f'{keyword_file}:"{save_path}",{keyword_error_size}:{format_local_size},{keyword_actual_size}:{format_sever_size},{keyword_link_status}:{failure_download}'
                               , level=LogLevel.warning)
                for _ in download_path:
                    os.remove(_)
                raise pyrogram.errors.exceptions.bad_request_400.BadRequest()

    elif isinstance(sever_size, int) and isinstance(download_path, str):  # 单文件
        local_size: int = os.path.getsize(download_path)
        format_local_size, format_sever_size = suitable_units_display(local_size), suitable_units_display(sever_size)
        save_path: str = os.path.join(save_directory, split_path(download_path)[1])
        if sever_size == local_size:
            # TODO: 根据下载的文件判断其类型对其精准分类计数:视频个数,图片个数
            _move_to_download_path(temp_save_path=download_path, save_path=save_directory)
            print_with_log(
                msg=f'{keyword_file}:"{save_path}",{keyword_size}:{format_local_size},{keyword_link_status}:{DownloadStatus.success.text}。',
                level=LogLevel.success)
        else:
            print_with_log(msg=
                           f'{keyword_file}:"{save_path}",{keyword_error_size}:{format_local_size},{keyword_actual_size}:{format_sever_size},{keyword_link_status}:{failure_download}'
                           , level=LogLevel.warning)
            os.remove(download_path)
            raise pyrogram.errors.exceptions.bad_request_400.BadRequest()


async def _extract_link_content(client, msg_link):
    comment_message = []
    is_comment = False
    if "?single" in msg_link:  # todo 如果用户只想下载组中的其一
        msg_link = msg_link.split("?single")[0]
    if "?comment" in msg_link:  # 链接中包含?comment表示用户需要同时下载评论中的媒体
        msg_link = msg_link.split("?comment")[0]
        is_comment = True
    msg_id = int(msg_link.split("/")[-1])
    if 't.me/c/' in msg_link:
        if 't.me/b/' in msg_link:
            chat_name = str(msg_link.split("/")[-2])
        else:
            chat_name = int('-100' + str(msg_link.split("/")[-2]))  # 得到频道的id
    else:
        chat_name = msg_link.split("/")[-2]  # 频道的名字

    if is_comment:
        # 如果用户需要同时下载媒体下面的评论,把评论中的所有信息放入列表一起返回
        async for comment in client.get_discussion_replies(chat_name, msg_id):
            comment_message.append(comment)

    return chat_name, msg_id, comment_message


async def _is_group(message) -> Any:
    try:
        return True, await message.get_media_group()
    except ValueError as e:
        return False, None if str(e) == "The message doesn't belong to a media group" else 0
        # v1.0.4 修改单文件无法下载问题return False, [] if str(e) == "The message doesn't belong to a media group" else 0
    except AttributeError:
        return None, None


async def _create_download_task(client, message, media_obj, temp_save_path, save_path, msg_link, link_type):
    sever_meta = getattr(message, media_obj)
    sever_size = getattr(sever_meta, 'file_size')
    actual_save_path = os.path.join(save_path, split_path(temp_save_path)[1])
    if is_exist(actual_save_path) and os.path.getsize(actual_save_path) == sever_size:  # 检测是否存在
        print_with_log(msg=
                       f'{keyword_link}:"{msg_link},{keyword_file}:"{split_path(temp_save_path)[1]}",{keyword_already_exist}:"{actual_save_path}",{keyword_link_status}:{skip_download}。',
                       level=LogLevel.info)
    else:
        file_meta = getattr(message, media_obj)
        file_id, msg_id = getattr(file_meta, 'file_id'), getattr(message, 'id')
        format_size = suitable_units_display(sever_size)
        print_with_log(msg=
                       f'{keyword_link}:"{msg_link}",{keyword_link_type}:{link_type},{keyword_id}:{msg_id},{keyword_size}:{format_size},{keyword_link_status}:{downloading}。',
                       level=LogLevel.info)
        task = asyncio.create_task(
            client.download_media(message=message,
                                  progress_args=(msg_link, os.path.basename(temp_save_path)),
                                  progress=_download_bar,
                                  file_name=temp_save_path))

        def call(future):
            if future.exception() is not None:
                print_with_log(msg=f'任务出错:{future.exception()}', level=LogLevel.error)
            else:
                _check_download_finish(sever_size=sever_size, download_path=temp_save_path,
                                       save_directory=save_path)

        task.add_done_callback(lambda future: call(future))
        return task


async def download_media_from_link(client: pyrogram.client.Client,
                                   msg_link: str,
                                   temp_folder=os.path.join(os.getcwd(), 'temp'),
                                   save_path=os.path.join(os.getcwd(), 'downloads')):
    tasks = set()
    try:
        chat_name, msg_id, is_download_comment = await _extract_link_content(client, msg_link)
        msg = await client.get_messages(chat_name, msg_id)  # 该消息的信息
        res, group = await _is_group(msg)
        if res or is_download_comment:
            group.extend(is_download_comment) if is_download_comment else 0
            link_type = LinkType.include_comment.text if is_download_comment else LinkType.group.text
            print_with_log(
                msg=f'{keyword_reading}:"{chat_name}",{keyword_link}"{msg_link}",{keyword_label}:{link_type}。',
                level=LogLevel.info)
            for msg_group in group:
                if msg_group.video:
                    temp_save_path = _get_temp_path(message=msg_group, media_obj='video', temp_folder=temp_folder)
                    task = await _create_download_task(client=client,
                                                       message=msg_group,
                                                       media_obj='video',
                                                       temp_save_path=temp_save_path,
                                                       save_path=save_path,
                                                       msg_link=msg_link,
                                                       link_type=link_type)
                    if task:
                        tasks.add(task)
                elif msg_group.photo:
                    temp_save_path = _get_temp_path(message=msg_group, media_obj='photo', temp_folder=temp_folder)
                    task = await _create_download_task(client=client,
                                                       message=msg_group,
                                                       media_obj='photo',
                                                       temp_save_path=temp_save_path,
                                                       save_path=save_path,
                                                       msg_link=msg_link,
                                                       link_type=link_type)
                    if task:
                        tasks.add(task)
        elif res is False and group is None:
            link_type = LinkType.single.text
            print_with_log(msg=f'正在读取频道"{chat_name}",中"{msg_link}"{link_type}中的内容。',
                           level=LogLevel.info)
            temp_save_path = _get_temp_path(message=msg, media_obj='video', temp_folder=temp_folder)
            if msg.video:
                task = await _create_download_task(client=client,
                                                   message=msg,
                                                   media_obj='video',
                                                   temp_save_path=temp_save_path,
                                                   save_path=save_path,
                                                   msg_link=msg_link,
                                                   link_type=link_type)
                if task:
                    tasks.add(task)
            elif msg.photo:
                temp_save_path = _get_temp_path(message=msg, media_obj='photo', temp_folder=temp_folder)
                task = await _create_download_task(client=client,
                                                   message=msg,
                                                   media_obj='photo',
                                                   temp_save_path=temp_save_path,
                                                   save_path=save_path,
                                                   msg_link=msg_link,
                                                   link_type=link_type)
                if task:
                    tasks.add(task)
        elif res is None and group is None:
            print_with_log(msg=f'{keyword_link}:"{msg_link}"消息不存在,频道已解散或未在频道中,{skip_download}。',
                           level=LogLevel.warning)

        elif res is None and group == 0:
            print_with_log(msg=f'读取"{msg_link}"时出现未知错误,{skip_download}。', level=LogLevel.error)
    except UnicodeEncodeError as e:
        print_with_log(msg=f'{keyword_link}:"{msg_link}"频道标题存在特殊字符,请移步终端下载!。原因:"{e}"',
                       level=LogLevel.error)
    except Exception as e:
        print_with_log(msg=f'{keyword_link}:"{msg_link}"消息不存在,频道已解散或未在频道中,{skip_download}。原因:"{e}"',
                       level=LogLevel.error)
    finally:
        return tasks


async def _download_bar(current, total, msg_link, file_name):
    format_current_size, format_total_size = suitable_units_display(current), suitable_units_display(total)
    # todo 加入颜色
    print(f"{msg_link}[{file_name}]({format_current_size}/{format_total_size}[{current * 100 / total:.1f}%])")


def _process_links(links: Any) -> List[str]:
    start_content: str = 'https://t.me/'
    msg_link_list: list = []
    if isinstance(links, str):
        if links.endswith('.txt') and os.path.isfile(links):
            with open(file=links, mode='r', encoding='UTF-8') as _:
                for link in [content.strip() for content in _.readlines()]:
                    if link.startswith(start_content):
                        msg_link_list.append(link)
                    else:
                        print_with_log(msg=f'"{link}"是一个非法链接,{keyword_link_status}:{skip_download}。',
                                       level=LogLevel.warning)
        elif not os.path.isfile(links):
            if os.path.exists(links):
                print_with_log(msg=f'读取"{links}"路径时出现未知错误。', level=LogLevel.error)
            else:
                print_with_log(msg=f'文件"{links}"不存在。', level=LogLevel.error)
        elif links.startswith(start_content):
            if 80 > len(links) - len(start_content) > 2:
                msg_link_list.append(links)
            else:
                print_with_log(msg=f'"{links}"是一个非法链接,{keyword_link_status}:{skip_download}。',
                               level=LogLevel.warning)
    elif isinstance(links, list):
        for single_link in links:
            try:
                if single_link.startswith(start_content) and 80 > len(single_link) - len(
                        start_content) > 2 and single_link not in msg_link_list:
                    msg_link_list.append(single_link)
                elif single_link in msg_link_list:
                    print_with_log(msg=f'"{single_link}"已存在,{keyword_link_status}:{skip_download}。',
                                   level=LogLevel.info)
                else:
                    print_with_log(msg=f'"{single_link}"是一个非法链接,{keyword_link_status}:{skip_download}。',
                                   level=LogLevel.warning)
            except AttributeError:
                print_with_log(msg=f'{single_link}是一个非法链接,{keyword_link_status}:{skip_download}。',
                               level=LogLevel.warning)
    if len(msg_link_list) > 0:
        return msg_link_list
    else:
        print_with_log('没有找到有效链接,程序已退出。', level=LogLevel.info)
        exit(0)


async def download_media_from_links(client: pyrogram.client.Client,
                                    links: List[str] or str,
                                    max_download_task: int = 3,
                                    temp_folder=os.path.join(os.getcwd(), 'temp'),
                                    save_path: str = os.path.join(os.getcwd(), 'downloads')):
    await client.start()
    print_meta(print_with_log)
    tasks = set()
    for link in _process_links(links=links):
        tasks = await download_media_from_link(client=client,
                                               msg_link=link,
                                               temp_folder=temp_folder,
                                               save_path=save_path)
    await asyncio.gather(*tasks)
