import pandas as pd
import io
from datetime import datetime


def read_excel_file(file):
    """
    读取Excel或CSV文件，自动检测中文编码
    :param file: Flask上传的文件对象
    :return: (data_list, error_message) 成功返回数据列表和None，失败返回None和错误信息
    """
    try:
        filename = file.filename.lower()

        # 读取文件内容到内存（避免多次读取文件指针问题）
        file_content = file.read()

        if filename.endswith('.csv'):
            # 中文CSV文件常见编码，按优先级尝试
            encodings = ['utf-8-sig', 'gbk', 'gb2312', 'cp936', 'iso-8859-1']

            for encoding in encodings:
                try:
                    # 使用BytesIO包装字节流
                    df = pd.read_csv(io.BytesIO(file_content), encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                # 所有编码都尝试失败
                return None, "CSV文件编码不支持，请转换为UTF-8或GBK格式"

        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            # Excel文件不需要编码处理
            df = pd.read_excel(io.BytesIO(file_content))

        else:
            return None, f"不支持的文件格式: {filename}"

        # 去除空行
        df = df.dropna(how='all')

        # 转换为字典列表
        data_list = df.to_dict('records')

        return data_list, None

    except Exception as e:
        return None, f"读取文件失败: {str(e)}"


def parse_date(date_value):
    """
    解析日期格式，统一转换为YYYY-MM-DD字符串
    """
    if pd.isna(date_value) or date_value is None or str(date_value).strip() == '':
        return None

    if isinstance(date_value, datetime):
        return date_value.strftime('%Y-%m-%d')

    try:
        # 尝试解析常见日期格式
        return pd.to_datetime(date_value).strftime('%Y-%m-%d')
    except:
        return str(date_value)


def parse_time(time_value, date_str=None):
    """
    解析时间格式，统一转换为MySQL datetime格式 YYYY-MM-DD HH:MM:SS
    :param time_value: 时间值，可以是单独的时间或完整的datetime
    :param date_str: 日期字符串（YYYY-MM-DD），如果time_value只有时间部分则使用此日期
    :return: 完整的datetime字符串或None
    """
    if pd.isna(time_value) or time_value is None or str(time_value).strip() == '':
        return None

    # 如果已经是datetime对象，直接格式化
    if isinstance(time_value, datetime):
        return time_value.strftime('%Y-%m-%d %H:%M:%S')

    time_str = str(time_value).strip()

    # 如果已经包含日期和时间，直接解析
    if ' ' in time_str or '-' in time_str or '/' in time_str:
        try:
            return pd.to_datetime(time_str).strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass

    # 如果只有时间部分，需要结合日期
    if date_str:
        try:
            # 组合日期和时间
            full_datetime = pd.to_datetime(f"{date_str} {time_str}")
            return full_datetime.strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass

    # 如果所有解析都失败，返回None（数据库允许NULL）
    return None