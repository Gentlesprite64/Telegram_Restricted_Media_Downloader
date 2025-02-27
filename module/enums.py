# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/2 0:59
# File:enums.py
import os
import base64
import ipaddress
from io import BytesIO

from enum import Enum

from module import console, log


class LinkType:
    SINGLE: str = 'single'
    GROUP: str = 'group'
    COMMENT: str = 'comment'

    def __iter__(self):
        for key, value in vars(self.__class__).items():
            if not key.startswith('__') and not callable(value):  # 排除特殊方法和属性
                yield value

    @staticmethod
    def t(text: str) -> str:
        translation = {
            LinkType.SINGLE: '单文件',
            LinkType.GROUP: '组文件',
            LinkType.COMMENT: '评论区文件',
        }
        if text in translation:
            return translation[text]
        else:
            return text


class DownloadType(Enum):
    VIDEO = 0
    PHOTO = 1
    DOCUMENT = 2

    @property
    def text(self) -> str:
        return {
            DownloadType.VIDEO: 'video',
            DownloadType.PHOTO: 'photo',
            DownloadType.DOCUMENT: 'document'
        }[self]

    @staticmethod
    def support_type() -> list:
        return [i.text for i in DownloadType]

    @staticmethod
    def t(text: 'DownloadType.text') -> str:
        translation = {
            DownloadType.VIDEO.text: '视频',
            DownloadType.PHOTO.text: '图片',
            DownloadType.DOCUMENT.text: '文档'
        }
        if text in translation:
            return translation[text]
        else:
            return text


class DownloadStatus(Enum):
    DOWNLOADING = 0
    SUCCESS = 1
    FAILURE = 2
    SKIP = 3
    RETRY = 4

    @property
    def text(self) -> str:
        return {
            DownloadStatus.DOWNLOADING: 'downloading',
            DownloadStatus.SUCCESS: 'success',
            DownloadStatus.FAILURE: 'failure',
            DownloadStatus.SKIP: 'skip',
            DownloadStatus.RETRY: 'retry'
        }[self]

    def __iter__(self):
        for key, value in vars(self.__class__).items():
            if not key.startswith('__') and not callable(value):  # 排除特殊方法和属性
                yield value

    @staticmethod
    def t(text: 'DownloadStatus.text', key_note: bool = False) -> str:
        translation = {
            DownloadStatus.DOWNLOADING.text: '下载中',
            DownloadStatus.SUCCESS.text: '成功',
            DownloadStatus.FAILURE.text: '失败',
            DownloadStatus.SKIP.text: '跳过',
            DownloadStatus.RETRY.text: '重试'
        }
        if text in translation:
            if key_note:
                return f'[{translation[text]}]'
            else:
                return translation[text]
        else:
            return text


class Status:
    DOWNLOADING = DownloadStatus.t(DownloadStatus.DOWNLOADING.text)
    SUCCESS = DownloadStatus.t(DownloadStatus.SUCCESS.text)
    FAILURE = DownloadStatus.t(DownloadStatus.FAILURE.text)
    SKIP = DownloadStatus.t(DownloadStatus.SKIP.text)


class _KeyWord:
    LINK: str = 'link'
    LINK_TYPE: str = 'link_type'
    SIZE: str = 'size'
    STATUS: str = 'status'
    FILE: str = 'file'
    ERROR_SIZE: str = 'error_size'
    ACTUAL_SIZE: str = 'actual_size'
    ALREADY_EXIST: str = 'already_exist'
    CHANNEL: str = 'channel'
    TYPE: str = 'type'
    REASON: str = 'reason'

    @staticmethod
    def t(text: str, key_note: bool = False) -> str:
        translation = {
            _KeyWord.LINK: '链接',
            _KeyWord.LINK_TYPE: '链接类型',
            _KeyWord.SIZE: '大小',
            _KeyWord.STATUS: '状态',
            _KeyWord.FILE: '文件',
            _KeyWord.ERROR_SIZE: '错误大小',
            _KeyWord.ACTUAL_SIZE: '实际大小',
            _KeyWord.ALREADY_EXIST: '已存在',
            _KeyWord.CHANNEL: '频道',
            _KeyWord.TYPE: '类型',
            _KeyWord.REASON: '原因'
        }

        if text in translation:
            if key_note:
                return f'[{translation[text]}]'
            else:
                return translation[text]
        else:
            return text


class KeyWord:
    LINK = _KeyWord.t(_KeyWord.LINK, True)
    LINK_TYPE = _KeyWord.t(_KeyWord.LINK_TYPE, True)
    SIZE = _KeyWord.t(_KeyWord.SIZE, True)
    STATUS = _KeyWord.t(_KeyWord.STATUS, True)
    FILE = _KeyWord.t(_KeyWord.FILE, True)
    ERROR_SIZE = _KeyWord.t(_KeyWord.ERROR_SIZE, True)
    ACTUAL_SIZE = _KeyWord.t(_KeyWord.ACTUAL_SIZE, True)
    ALREADY_EXIST = _KeyWord.t(_KeyWord.ALREADY_EXIST, True)
    CHANNEL = _KeyWord.t(_KeyWord.CHANNEL, True)
    TYPE = _KeyWord.t(_KeyWord.TYPE, True)
    REASON = _KeyWord.t(_KeyWord.REASON, False)


class Extension:
    PHOTO = {'image/avif': 'avif',
             'image/bmp': 'bmp',
             'image/gif': 'gif',
             'image/ief': 'ief',
             'image/jpg': 'jpg',
             'image/jpeg': 'jpeg',
             'image/heic': 'heic',
             'image/heif': 'heif',
             'image/png': 'png',
             'image/svg+xml': 'svg',
             'image/tiff': 'tif',
             'image/vnd.microsoft.icon': 'ico',
             'image/x-cmu-raster': 'ras',
             'image/x-portable-anymap': 'pnm',
             'image/x-portable-bitmap': 'pbm',
             'image/x-portable-graymap': 'pgm',
             'image/x-portable-pixmap': 'ppm',
             'image/x-rgb': 'rgb',
             'image/x-xbitmap': 'xbm',
             'image/x-xpixmap': 'xpm',
             'image/x-xwindowdump': 'xwd'}
    VIDEO = {'video/mp4': 'mp4',
             'video/mpeg': 'mpg',
             'video/quicktime': 'qt',
             'video/webm': 'webm',
             'video/x-msvideo': 'avi',
             'video/x-sgi-movie': 'movie',
             'video/x-matroska': 'mkv'}


class GradientColor:
    # 生成渐变色:https://photokit.com/colors/color-gradient/?lang=zh
    BLUE2PURPLE_14 = ['#0ebeff',
                      '#21b4f9',
                      '#33abf3',
                      '#46a1ed',
                      '#5898e8',
                      '#6b8ee2',
                      '#7d85dc',
                      '#907bd6',
                      '#a272d0',
                      '#b568ca',
                      '#c75fc5',
                      '#da55bf',
                      '#ec4cb9',
                      '#ff42b3']
    GREEN2PINK_11 = ['#00ff40',
                     '#14f54c',
                     '#29eb58',
                     '#3de064',
                     '#52d670',
                     '#66cc7c',
                     '#7ac288',
                     '#8fb894',
                     '#a3ada0',
                     '#b8a3ac',
                     '#cc99b8']
    GREEN2BLUE_10 = ['#84fab0',
                     '#85f6b8',
                     '#86f1bf',
                     '#88edc7',
                     '#89e9ce',
                     '#8ae4d6',
                     '#8be0dd',
                     '#8ddce5',
                     '#8ed7ec',
                     '#8fd3f4']
    YELLOW2GREEN_10 = ['#d4fc79',
                       '#cdfa7d',
                       '#c6f782',
                       '#bff586',
                       '#b8f28b',
                       '#b2f08f',
                       '#abed94',
                       '#a4eb98',
                       '#9de89d',
                       '#96e6a1']
    new_life = ['#43e97b',
                '#42eb85',
                '#41ed8f',
                '#3fee9a',
                '#3ef0a4',
                '#3df2ae',
                '#3cf4b8',
                '#3af5c3',
                '#39f7cd',
                '#38f9d7']
    ORANGE2YELLOW_15 = ['#f08a5d',
                        '#f1915e',
                        '#f1985f',
                        '#f29f60',
                        '#f3a660',
                        '#f3ad61',
                        '#f4b462',
                        '#f5bc63',
                        '#f5c364',
                        '#f6ca65',
                        '#f6d166',
                        '#f7d866',
                        '#f8df67',
                        '#f8e668',
                        '#f9ed69']

    @staticmethod
    def __extend_gradient_colors(colors: list, target_length: int) -> list:
        extended_colors = colors[:]
        while len(extended_colors) < target_length:
            # 添加原列表（除最后一个元素外）的逆序
            extended_colors.extend(colors[-2::-1])
            # 如果仍然不够长，继续添加正序部分
            if len(extended_colors) < target_length:
                extended_colors.extend(colors[:-1])
        return extended_colors[:target_length]

    @staticmethod
    def gen_gradient_text(text: str, gradient_color: list) -> str:
        """当渐变色列表小于文字长度时,翻转并扩展当前列表。"""
        text_lst: list = [i for i in text]
        text_lst_len: int = len(text_lst)
        gradient_color_len: int = len(gradient_color)
        if text_lst_len > gradient_color_len:
            # 扩展颜色列表以适应文本长度
            gradient_color = GradientColor.__extend_gradient_colors(gradient_color, text_lst_len)
        result: str = ''
        for i in range(text_lst_len):
            result += f'[{gradient_color[i]}]{text_lst[i]}[/{gradient_color[i]}]'
        return result

    @staticmethod
    def __hex_to_rgb(hex_color: str) -> tuple:
        """将十六进制颜色值转换为RGB元组。"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def __rgb_to_hex(r: int, g: int, b: int) -> str:
        """将RGB元组转换为十六进制颜色值。"""
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def generate_gradient(start_color: str, end_color: str, steps: int) -> list:
        """根据起始和结束颜色生成颜色渐变列表。"""
        steps = 2 if steps <= 1 else steps
        # 转换起始和结束颜色为RGB
        start_rgb = GradientColor.__hex_to_rgb(start_color)
        end_rgb = GradientColor.__hex_to_rgb(end_color)
        # 生成渐变色列表
        gradient_color: list = []
        for i in range(steps):
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (steps - 1))
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (steps - 1))
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (steps - 1))
            gradient_color.append(GradientColor.__rgb_to_hex(r, g, b))

        return gradient_color


class Banner:
    A = r'''
       ______           __  __                     _ __          
      / ____/__  ____  / /_/ /__  _________  _____(_) /____      
     / / __/ _ \/ __ \/ __/ / _ \/ ___/ __ \/ ___/ / __/ _ \     
    / /_/ /  __/ / / / /_/ /  __(__  ) /_/ / /  / / /_/  __/     
    \____/\___/_/ /_/\__/_/\___/____/ .___/_/  /_/\__/\___/      
                                   /_/                           
        '''
    B = r'''
    ╔═╗┌─┐┌┐┌┌┬┐┬  ┌─┐┌─┐┌─┐┬─┐┬┌┬┐┌─┐  
    ║ ╦├┤ │││ │ │  ├┤ └─┐├─┘├┬┘│ │ ├┤   
    ╚═╝└─┘┘└┘ ┴ ┴─┘└─┘└─┘┴  ┴└─┴ ┴ └─┘  
        '''
    C = r'''
     ██████╗ ███████╗███╗   ██╗████████╗██╗     ███████╗███████╗██████╗ ██████╗ ██╗████████╗███████╗    
    ██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██║     ██╔════╝██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝██╔════╝    
    ██║  ███╗█████╗  ██╔██╗ ██║   ██║   ██║     █████╗  ███████╗██████╔╝██████╔╝██║   ██║   █████╗      
    ██║   ██║██╔══╝  ██║╚██╗██║   ██║   ██║     ██╔══╝  ╚════██║██╔═══╝ ██╔══██╗██║   ██║   ██╔══╝      
    ╚██████╔╝███████╗██║ ╚████║   ██║   ███████╗███████╗███████║██║     ██║  ██║██║   ██║   ███████╗    
     ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝           
            '''
    D = r'''                                                                          
                                        ,,                                       ,,                    
  .g8"""bgd                      mm   `7MM                                       db   mm               
.dP'     `M                      MM     MM                                            MM               
dM'       `   .gP"Ya `7MMpMMMb.mmMMmm   MM  .gP"Ya  ,pP"Ybd `7MMpdMAo.`7Mb,od8 `7MM mmMMmm .gP"Ya      
MM           ,M'   Yb  MM    MM  MM     MM ,M'   Yb 8I   `"   MM   `Wb  MM' "'   MM   MM  ,M'   Yb     
MM.    `7MMF'8M""""""  MM    MM  MM     MM 8M"""""" `YMMMa.   MM    M8  MM       MM   MM  8M""""""     
`Mb.     MM  YM.    ,  MM    MM  MM     MM YM.    , L.   I8   MM   ,AP  MM       MM   MM  YM.    ,     
  `"bmmmdPY   `Mbmmd'.JMML  JMML.`Mbmo.JMML.`Mbmmd' M9mmmP'   MMbmmd' .JMML.   .JMML. `Mbmo`Mbmmd'     
                                                              MM                                       
                                                            .JMML.                                     
    '''


class Validator:
    @staticmethod
    def is_valid_api_id(api_id: str, valid_length: int = 32) -> bool:
        try:
            if len(api_id) < valid_length:
                if api_id.isdigit():
                    return True
                else:
                    log.warning(f'意外的参数:"{api_id}",不是「纯数字」请重新输入!')
                    return False
            else:
                log.warning(f'意外的参数,填写的"{api_id}"可能是「api_hash」,请填入正确的「api_id」!')
                return False
        except (AttributeError, TypeError):
            log.error('手动编辑config.yaml时,api_id需要有引号!')
            return False

    @staticmethod
    def is_valid_api_hash(api_hash: str, valid_length: int = 32) -> bool:
        return len(str(api_hash)) == valid_length

    @staticmethod
    def is_valid_bot_token(bot_token: str, valid_format: str = ':') -> bool:
        if valid_format in bot_token:
            return True
        else:
            return False

    @staticmethod
    def is_valid_links_file(file_path: str, valid_format: str = '.txt') -> bool:
        file_path = os.path.normpath(file_path)
        return os.path.isfile(file_path) and file_path.endswith(valid_format)

    @staticmethod
    def is_valid_save_path(save_path: str) -> bool:
        if not os.path.exists(save_path):
            while True:
                try:
                    question = console.input(f'目录:"{save_path}"不存在,是否创建? - 「y|n」(默认y):').strip().lower()
                    if question in ('y', ''):
                        os.makedirs(save_path, exist_ok=True)
                        console.log(f'成功创建目录:"{save_path}"')
                        break
                    elif question == 'n':
                        break
                    else:
                        log.warning(f'意外的参数:"{question}",支持的参数 - 「y|n」')
                except Exception as e:
                    log.error(f'意外的错误,原因:"{e}"')
                    break
        return os.path.isdir(save_path)

    @staticmethod
    def is_valid_max_download_task(max_tasks: int) -> bool:
        try:
            return int(max_tasks) > 0
        except ValueError:
            return False
        except Exception as e:
            log.error(f'意外的错误,原因:"{e}"')

    @staticmethod
    def is_valid_enable_proxy(enable_proxy: str or bool) -> bool:
        if enable_proxy in ('y', 'n'):
            return True

    @staticmethod
    def is_valid_scheme(scheme: str, valid_format: list) -> bool:
        return scheme in valid_format

    @staticmethod
    def is_valid_hostname(hostname: str) -> bool:
        return isinstance(ipaddress.ip_address(hostname), ipaddress.IPv4Address)

    @staticmethod
    def is_valid_port(port: int) -> bool:
        try:
            return 0 < int(port) <= 65535
        except ValueError:  # 处理非整数字符串的情况
            return False
        except TypeError:  # 处理传入非数字类型的情况
            return False
        except Exception as e:
            log.error(f'意外的错误,原因:"{e}"')
            return False

    @staticmethod
    def is_valid_download_type(dtype: int or str) -> bool:
        try:
            _dtype = int(dtype) if isinstance(dtype, str) else dtype
            return 0 < _dtype < 4
        except ValueError:  # 处理非整数字符串的情况
            return False
        except TypeError:  # 处理传入非数字类型的情况
            return False
        except Exception as e:
            log.error(f'意外的错误,原因:"{e}"')
            return False


class QrcodeRender:
    @staticmethod
    def render_2by1(qr_map) -> str:
        blocks_2by1: list = ['█', '▀', '▄', ' ']
        output: str = ''
        for row in range(0, len(qr_map), 2):
            for col in range(0, len(qr_map[0])):
                pixel_cur = qr_map[row][col]
                pixel_below = 1
                if row < len(qr_map) - 1:
                    pixel_below = qr_map[row + 1][col]
                pixel_encode = pixel_cur << 1 | pixel_below
                output += blocks_2by1[pixel_encode]
            output += '\n'
        return output[:-1]

    @staticmethod
    def render_3by2(qr_map) -> str:
        blocks_3by2: list = [
            '█', '🬝', '🬬', '🬎', '🬴', '🬕', '🬥', '🬆',

            '🬸', '🬙', '🬨', '🬊', '🬰', '🬒', '🬡', '🬂',

            '🬺', '🬛', '🬪', '🬌', '🬲', '▌', '🬣', '🬄',

            '🬶', '🬗', '🬧', '🬈', '🬮', '🬐', '🬟', '🬀',

            '🬻', '🬜', '🬫', '🬍', '🬳', '🬔', '🬤', '🬅',

            '🬷', '🬘', '▐', '🬉', '🬯', '🬑', '🬠', '🬁',

            '🬹', '🬚', '🬩', '🬋', '🬱', '🬓', '🬢', '🬃',

            '🬵', '🬖', '🬦', '🬇', '🬭', '🬏', '🬞', ' ',
        ]

        output: str = ''

        def get_qr_map(r, c):
            return 1 if r >= len(qr_map) or c >= len(qr_map[0]) else qr_map[r][c]

        for row in range(0, len(qr_map), 3):
            for col in range(0, len(qr_map[0]), 2):
                pixel5 = qr_map[row][col]
                pixel4 = get_qr_map(row, col + 1)
                pixel3 = get_qr_map(row + 1, col)
                pixel2 = get_qr_map(row + 1, col + 1)
                pixel1 = get_qr_map(row + 2, col)
                pixel0 = get_qr_map(row + 2, col + 1)
                pixel_encode = pixel5 << 5 | pixel4 << 4 | pixel3 << 3 | pixel2 << 2 | pixel1 << 1 | pixel0
                output += blocks_3by2[pixel_encode]
            output += '\n'

        return output[:-1]


class ProcessConfig:
    @staticmethod
    def set_dtype(_dtype) -> list:
        i_dtype = int(_dtype)  # 因为终端输入是字符串，这里需要转换为整数。
        if i_dtype == 1:
            return [DownloadType.VIDEO.text]
        elif i_dtype == 2:
            return [DownloadType.PHOTO.text]
        elif i_dtype == 3:
            return [DownloadType.VIDEO.text, DownloadType.PHOTO.text]

    @staticmethod
    def get_dtype(download_dtype: list) -> dict:
        """获取所需下载文件的类型。"""
        if DownloadType.DOCUMENT.text in download_dtype:
            download_dtype.remove(DownloadType.DOCUMENT.text)
        dt_length = len(download_dtype)
        if dt_length == 1:
            dtype: str = download_dtype[0]
            if dtype == DownloadType.VIDEO.text:
                return {'video': True, 'photo': False}
            elif dtype == DownloadType.PHOTO.text:
                return {'video': False, 'photo': True}
        elif dt_length == 2:
            return {'video': True, 'photo': True}
        return {'error': True}

    @staticmethod
    def stdio_style(key: str, color=None) -> str:
        """控制用户交互时打印出不同的颜色(渐变)。"""
        if color is None:
            color = GradientColor.ORANGE2YELLOW_15
        _stdio_queue: dict = {'api_id': 0,
                              'api_hash': 1,
                              'bot_token': 2,
                              'links': 3,
                              'save_directory': 4,
                              'max_download_task': 5,
                              'download_type': 6,
                              'is_shutdown': 7,
                              'enable_proxy': 8,
                              'config_proxy': 9,
                              'scheme': 10,
                              'hostname': 11,
                              'port': 12,
                              'proxy_authentication': 13
                              }
        return color[_stdio_queue.get(key)]

    @staticmethod
    def is_proxy_input(proxy_config: dict) -> bool:
        """检测代理配置是否需要用户输入。"""
        result: bool = False
        basic_truth_table: list = []
        advance_account_truth_table: list = []
        if proxy_config.get('enable_proxy') is False:  # 检测打开了代理但是代理配置错误。
            return False
        for _ in proxy_config.items():
            if _[0] in ['scheme', 'port', 'hostname']:
                basic_truth_table.append(_[1])
            if _[0] in ['username', 'password']:
                advance_account_truth_table.append(_[1])
        if all(basic_truth_table) is False:
            console.print('请配置代理!', style=ProcessConfig.stdio_style('config_proxy'))
            result: bool = True
        if any(advance_account_truth_table) and all(advance_account_truth_table) is False:
            log.warning('代理账号或密码未输入!')
            result: bool = True
        return result

    @staticmethod
    def get_proxy_info(proxy_config: dict) -> dict:
        return {'scheme': proxy_config.get('scheme', '未知'),
                'hostname': proxy_config.get('hostname', '未知'),
                'port': proxy_config.get('port', '未知')}


class GetStdioParams:
    UNDEFINED = '无'

    @staticmethod
    def get_is_ki_save_config(valid_format: str = 'y|n') -> dict:
        while True:
            is_save_config: str = console.input(
                f'「退出提示」是否需要保存当前已填写的参数? - 「{valid_format}」:').strip().lower()
            if is_save_config == 'y':
                return {'is_ki_save_config': True}
            elif is_save_config == 'n':
                return {'is_ki_save_config': False}
            else:
                log.warning(f'意外的参数:"{is_save_config}",支持的参数 - 「{valid_format}」')

    @staticmethod
    def get_is_re_config(valid_format: str = 'y|n') -> dict:
        while True:
            is_re_config: str = console.input(
                f'检测到已配置完成的配置文件,是否需要重新配置?(之前的配置文件将为你备份到当前目录下) - 「{valid_format}」(默认n):').strip().lower()
            if is_re_config == 'y':
                return {'is_re_config': True}
            elif is_re_config in ('n', ''):
                return {'is_re_config': False}
            else:
                log.warning(f'意外的参数:"{is_re_config}",支持的参数 - 「{valid_format}」(默认n)')

    @staticmethod
    def get_is_change_account(valid_format: str = 'y|n') -> dict:
        style: str = '#FF4689'
        while True:
            is_change_account = console.input('是否需要切换账号? - 「y|n」(默认n):').strip().lower()
            if is_change_account in ('n', ''):
                console.print('用户不需要切换「账号」。', style=style)
                return {'is_change_account': False}
            elif is_change_account == 'y':
                console.print('用户需要切换「账号」。', style=style)
                return {'is_change_account': True}
            else:
                log.warning(f'意外的参数:"{is_change_account}",支持的参数 - 「{valid_format}」!')

    @staticmethod
    def get_api_id(last_record: str) -> dict:
        while True:
            api_id = console.input(
                f'请输入「api_id」上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」:').strip()
            if api_id == '' and last_record is not None:
                api_id = last_record
            if Validator.is_valid_api_id(api_id):
                console.print(f'已设置「api_id」为:「{api_id}」', style=ProcessConfig.stdio_style('api_id'))
                return {'api_id': api_id, 'record_flag': True}

    @staticmethod
    def get_api_hash(last_record: str, valid_length: int = 32) -> dict:
        while True:
            api_hash = console.input(
                f'请输入「api_hash」上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」:').strip().lower()
            if api_hash == '' and last_record is not None:
                api_hash = last_record
            if Validator.is_valid_api_hash(api_hash, valid_length):
                console.print(f'已设置「api_hash」为:「{api_hash}」', style=ProcessConfig.stdio_style('api_hash'))
                return {'api_hash': api_hash, 'record_flag': True}
            else:
                log.warning(f'意外的参数:"{api_hash}",不是一个「{valid_length}位」的「值」!请重新输入!')

    @staticmethod
    def get_enable_bot(valid_format: str = 'y|n') -> dict:
        while True:
            enable_bot = console.input('是否启用「机器人」(需要提供bot_token)? - 「y|n」(默认n):').strip().lower()
            if enable_bot in ('n', ''):
                console.print(f'已设置为不启用「机器人」。', style=ProcessConfig.stdio_style('bot_token'))
                return {'enable_bot': False}
            elif enable_bot == 'y':
                console.print(f'请配置「bot_token」。', style=ProcessConfig.stdio_style('bot_token'))
                return {'enable_bot': True}
            else:
                log.warning(f'意外的参数:"{enable_bot}",支持的参数 - 「{valid_format}」!')

    @staticmethod
    def get_bot_token(last_record: str, valid_format: str = ':') -> dict:
        while True:
            bot_token = console.input(
                f'请输入当前账号的「bot_token」上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」:').strip()
            if bot_token == '' and last_record is not None:
                bot_token = last_record
            if Validator.is_valid_bot_token(bot_token, valid_format):
                console.print(f'已设置「bot_token」为:「{bot_token}」', style=ProcessConfig.stdio_style('bot_token'))
                return {'bot_token': bot_token, 'record_flag': True}
            else:
                log.warning(f'意外的参数:"{bot_token}",「bot_token」中需要包含":",请重新输入!')

    @staticmethod
    def get_links(last_record: str, valid_format: str = '.txt') -> dict:
        # 输入需要下载的媒体链接文件路径,确保文件存在。
        links_file_path = None
        while True:
            try:
                links_file_path = console.input(
                    f'请输入需要下载的媒体链接的「完整路径」。上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」'
                    f'格式 - 「{valid_format}」:').strip()
                if links_file_path == '' and last_record is not None:
                    links_file_path = last_record
                if Validator.is_valid_links_file(links_file_path, valid_format):
                    console.print(f'已设置「links」为:「{links_file_path}」', style=ProcessConfig.stdio_style('links'))
                    return {'links': links_file_path, 'record_flag': True}
                elif not os.path.normpath(links_file_path).endswith('.txt'):
                    log.warning(f'意外的参数:"{links_file_path}",文件路径必须以「{valid_format}」结尾,请重新输入!')
                else:
                    log.warning(
                        f'意外的参数:"{links_file_path}",文件「必须存在」,请重新输入!')
            except Exception as _e:
                log.warning(
                    f'意外的参数:"{links_file_path}",文件路径必须以「{valid_format}」结尾,并且「必须存在」,请重新输入!{KeyWord.REASON}:"{_e}"')

    @staticmethod
    def get_save_directory(last_record) -> dict:
        # 输入媒体保存路径,确保是一个有效的目录路径。
        while True:
            save_directory = console.input(
                f'请输入媒体「保存路径」。上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」:').strip()
            if save_directory == '' and last_record is not None:
                save_directory = last_record
            if Validator.is_valid_save_path(save_directory):
                console.print(f'已设置「save_directory」为:「{save_directory}」',
                              style=ProcessConfig.stdio_style('save_directory'))
                return {'save_directory': save_directory, 'record_flag': True}
            elif os.path.isfile(save_directory):
                log.warning(f'意外的参数:"{save_directory}",指定的路径是一个文件并非目录,请重新输入!')
            else:
                log.warning(f'意外的参数:"{save_directory}",指定的路径无效或不是一个目录,请重新输入!')

    @staticmethod
    def get_max_download_task(last_record) -> dict:
        # 输入最大下载任务数,确保是一个整数且不超过特定限制。
        while True:
            try:
                max_download_task = console.input(
                    f'请输入「最大下载任务数」。上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」'
                    f',值过高可能会导致网络相关问题,建议默认{"(默认3)" if last_record is None else ""}:').strip()
                if max_download_task == '' and last_record is not None:
                    max_download_task = last_record
                if max_download_task == '':
                    max_download_task = 3
                if Validator.is_valid_max_download_task(max_download_task):
                    console.print(f'已设置「max_download_task」为:「{max_download_task}」',
                                  style=ProcessConfig.stdio_style('max_download_task'))
                    return {'max_download_task': int(max_download_task), 'record_flag': True}
                else:
                    log.warning(f'意外的参数:"{max_download_task}",任务数必须是「正整数」,请重新输入!')
            except Exception as _e:
                log.error(f'意外的错误,{KeyWord.REASON}:"{_e}"')

    @staticmethod
    def get_download_type(last_record: list or None) -> dict:

        if isinstance(last_record, list):
            res: dict = ProcessConfig.get_dtype(download_dtype=last_record)
            if len(res) == 1:
                last_record = None
            elif res.get('video') and res.get('photo') is False:
                last_record = 1
            elif res.get('video') is False and res.get('photo'):
                last_record = 2
            elif res.get('video') and res.get('photo'):
                last_record = 3

        while True:
            download_type = console.input(
                f'输入需要下载的「媒体类型」。上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」'
                f'格式 - 「1.视频 2.图片 3.视频和图片」{"(默认3)" if last_record is None else ""}:').strip()
            if download_type == '' and last_record is not None:
                download_type = last_record
            if download_type == '':
                download_type = 3
            if Validator.is_valid_download_type(download_type):
                console.print(f'已设置「download_type」为:「{download_type}」',
                              style=ProcessConfig.stdio_style('download_type'))
                return {'download_type': ProcessConfig.set_dtype(_dtype=download_type), 'record_flag': True}
            else:
                log.warning(f'意外的参数:"{download_type}",支持的参数 - 「1或2或3」')

    @staticmethod
    def get_is_shutdown(last_record: str, valid_format: str = 'y|n') -> dict:
        _style: str = ProcessConfig.stdio_style('is_shutdown')
        if last_record:
            last_record: str = 'y'
        elif last_record is False:
            last_record: str = 'n'
        else:
            last_record = GetStdioParams.UNDEFINED
        t = f'已设置「is_shutdown」为:「y」,下载完成后将自动关机!'  # v1.3.0 修复配置is_shutdown参数时显示错误。
        f = f'已设置「is_shutdown」为:「n」'
        while True:
            try:
                is_shutdown = console.input(
                    f'下载完成后是否「自动关机」。上一次的记录是:「{last_record}」 - 「{valid_format}」'
                    f'{"(默认n)" if last_record == GetStdioParams.UNDEFINED else ""}:').strip().lower()
                if is_shutdown == '' and last_record != GetStdioParams.UNDEFINED:
                    if last_record == 'y':
                        console.print(t, style=_style)
                        return {'is_shutdown': True, 'record_flag': True}
                    elif last_record == 'n':
                        console.print(f, style=_style)
                        return {'is_shutdown': False, 'record_flag': True}

                elif is_shutdown == 'y':
                    console.print(t, style=_style)
                    return {'is_shutdown': True, 'record_flag': True}
                elif is_shutdown in ('n', ''):
                    console.print(f, style=_style)
                    return {'is_shutdown': False, 'record_flag': True}
                else:
                    log.warning(f'意外的参数:"{is_shutdown}",支持的参数 - 「{valid_format}」')

            except Exception as _e:
                log.error(f'意外的错误,{KeyWord.REASON}:"{_e}"')

    @staticmethod
    def get_enable_proxy(last_record: str or bool, valid_format: str = 'y|n') -> dict:
        if last_record:
            ep_notice: str = 'y' if last_record else 'n'
        else:
            ep_notice: str = GetStdioParams.UNDEFINED
        while True:  # 询问是否开启代理。
            enable_proxy = console.input(
                f'是否需要使用「代理」。上一次的记录是:「{ep_notice}」'
                f'格式 - 「{valid_format}」{"(默认n)" if ep_notice == GetStdioParams.UNDEFINED else ""}:').strip().lower()
            if enable_proxy == '' and last_record is not None:
                if last_record is True:
                    enable_proxy = 'y'
                elif last_record is False:
                    enable_proxy = 'n'
            elif enable_proxy == '':
                enable_proxy = 'n'
            if Validator.is_valid_enable_proxy(enable_proxy):
                if enable_proxy == 'y':
                    console.print(f'已设置「enable_proxy」为:「{enable_proxy}」',
                                  style=ProcessConfig.stdio_style('enable_proxy'))
                    return {'enable_proxy': True, 'record_flag': True}
                elif enable_proxy == 'n':
                    console.print(f'已设置「enable_proxy」为:「{enable_proxy}」',
                                  style=ProcessConfig.stdio_style('enable_proxy'))
                    return {'enable_proxy': False, 'record_flag': True}
            else:
                log.error(f'意外的参数:"{enable_proxy}",请输入有效参数!支持的参数 - 「{valid_format}」!')

    @staticmethod
    def get_scheme(last_record: str, valid_format: list) -> dict:
        if valid_format is None:
            valid_format = ['http', 'socks4', 'socks5']
        fmt_valid_format = '|'.join(valid_format)
        while True:  # v1.3.0 修复代理配置scheme参数配置抛出AttributeError。
            scheme = console.input(
                f'请输入「代理类型」。上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」'
                f'格式 - 「{fmt_valid_format}」:').strip().lower()
            if scheme == '' and last_record is not None:
                scheme = last_record
            if Validator.is_valid_scheme(scheme, valid_format):
                console.print(f'已设置「scheme」为:「{scheme}」', style=ProcessConfig.stdio_style('scheme'))
                return {'scheme': scheme, 'record_flag': True}
            else:
                log.warning(
                    f'意外的参数:"{scheme}",请输入有效的代理类型!支持的参数 - 「{fmt_valid_format}」!')

    @staticmethod
    def get_hostname(proxy_config: dict, last_record: str, valid_format: str = 'x.x.x.x'):
        hostname = None
        while True:
            scheme, _, __ = ProcessConfig.get_proxy_info(proxy_config).values()
            # 输入代理IP地址。
            try:
                hostname = console.input(
                    f'请输入代理类型为:"{scheme}"的「ip地址」。上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」'
                    f'格式 - 「{valid_format}」:').strip()
                if hostname == '' and last_record is not None:
                    hostname = last_record
                if Validator.is_valid_hostname(hostname):
                    console.print(f'已设置「hostname」为:「{hostname}」', style=ProcessConfig.stdio_style('hostname'))
                    return {'hostname': hostname, 'record_flag': True}
            except ValueError:
                log.warning(
                    f'"{hostname}"不是一个「ip地址」,请输入有效的ipv4地址!支持的参数 - 「{valid_format}」!')

    @staticmethod
    def get_port(proxy_config: dict, last_record: str, valid_format: str = '0~65535'):
        port = None
        # 输入代理端口。
        while True:
            try:  # hostname,scheme可能出现None。
                scheme, hostname, __ = ProcessConfig.get_proxy_info(proxy_config).values()
                port = console.input(
                    f'请输入ip地址为:"{hostname}",代理类型为:"{scheme}"的「代理端口」。'
                    f'上一次的记录是:「{last_record if last_record else GetStdioParams.UNDEFINED}」'
                    f'格式 - 「{valid_format}」:').strip()
                if port == '' and last_record is not None:
                    port = last_record
                if Validator.is_valid_port(port):
                    console.print(f'已设置「port」为:「{port}」', style=ProcessConfig.stdio_style('port'))
                    return {'port': int(port), 'record_flag': True}
                else:
                    log.warning(f'意外的参数:"{port}",端口号必须在「{valid_format}」之间!')
            except ValueError:
                log.warning(f'意外的参数:"{port}",请输入一个有效的整数!支持的参数 - 「{valid_format}」')
            except Exception as e:
                log.error(f'意外的错误,{KeyWord.REASON}:"{e}"')

    @staticmethod
    def get_proxy_authentication():
        # 是否需要认证。
        style = ProcessConfig.stdio_style('proxy_authentication')
        valid_format: str = 'y|n'
        while True:
            is_proxy = console.input(f'代理是否需要「认证」? - 「{valid_format}」(默认n):').strip().lower()
            if is_proxy == 'y':
                username = console.input('请输入「账号」:').strip()
                password = console.input('请输入「密码」:').strip()
                console.print(f'已设置为:「代理需要认证」', style=style)
                return {'username': username, 'password': password, 'record_flag': True}
            elif is_proxy in ('n', ''):
                console.print(f'已设置为:「代理不需要认证」', style=style)
                return {'username': None, 'password': None, 'record_flag': True}
            else:
                log.warning(f'意外的参数:"{is_proxy}",支持的参数 - 「{valid_format}」!')


class BotCommandText:
    HELP = ('help', '展示可用命令。')
    DOWNLOAD = ('download', '分配新的下载任务。`/download https://t.me/x/x`')
    TABLE = ('table', '在终端输出当前下载情况的统计信息。')
    EXIT = ('exit', '退出软件。')

    @staticmethod
    def with_description(text: tuple) -> str:
        return f'/{text[0]} - {text[1]}'


class BotCallbackText:
    PAY = 'pay'
    LINK_TABLE = 'link_table'
    COUNT_TABLE = 'count_table'
    BACK_HELP = 'back_help'

    def __iter__(self):
        for key, value in vars(self.__class__).items():
            if not key.startswith('__') and not callable(value):  # 排除特殊方法和属性
                yield value


class BotMessage:
    RIGHT = '✅以下链接已创建下载任务:\n'
    EXIST = '⚠️以下链接已存在已被移除:\n'
    INVALID = '🚫以下链接不合法已被移除:\n'


class Base64Image:
    pay = b'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'

    @staticmethod
    def base64_to_binary_io(base64_string):
        binary_data = base64.b64decode(base64_string)
        binary_io = BytesIO(binary_data)
        return binary_io
