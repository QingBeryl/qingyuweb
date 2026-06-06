import pandas as pd
from bps.attendance_bp.dao.attendance_dao import get_all_records, insert_one, by_date, by_student, get_all_students_name_id, get_all_classes
from bps.attendance_bp.dao.students_dao import get_all_students
from bps.attendance_bp.utils.excel_util import *

def process_index_data():
    records = get_all_records()
    n = l = t = a = 0
    for r in records:
        s = r['status']
        if s == '正常': n += 1
        elif s == '迟到': l += 1
        elif s == '请假': t += 1
        elif s == '未到': a += 1
    return {"records": records, "normal": n, "late": l, "leave": t, "absent": a}

def do_import_service(files, recorder, student_class):
    """
    完全对齐本地脚本逻辑的考勤导入业务逻辑
    数据库表：attendance
    支持两种格式：
    1. 原始导出：姓名、记录时间、状态（支持空时间和"——"）
    2. 标准格式：student_id、attend_date、attend_type、check_time、status
    """
    total_success = 0
    total_failed = 0
    error_messages = []

    # 数据库ENUM类型允许的值（严格匹配）
    ALLOWED_ATTEND_TYPES = {'早自习', '晚自习'}
    ALLOWED_STATUSES = {'正常', '迟到', '未到', '请假'}

    # 自动兼容单/多文件
    file_list = []
    if files is None:
        pass
    elif hasattr(files, 'filename'):
        file_list = [files]
    elif isinstance(files, (list, tuple)):
        file_list = [f for f in files if f and hasattr(f, 'filename')]
    else:
        try:
            file_list = list(files)
        except:
            pass

    if not file_list:
        return "错误：没有选择任何文件"

    # 预加载班级学生映射（仅在需要姓名匹配时使用）
    name_to_id = None
    try:
        students = get_all_students_name_id(student_class)
        if students:
            name_to_id = {student['name']: str(student['student_id']) for student in students}
    except Exception as e:
        return f"获取班级学生数据失败: {str(e)}"

    # 处理每个文件
    for file in file_list:
        filename = file.filename
        data_list, error = read_excel_file(file)

        if error:
            total_failed += 1
            error_messages.append(f"文件[{filename}]读取失败: {error}")
            continue

        if not data_list:
            total_failed += 1
            error_messages.append(f"文件[{filename}]没有有效数据")
            continue

        # 自动检测文件格式
        first_row = data_list[0]
        columns = [str(key).strip().lower() for key in first_row.keys()]

        is_standard_format = 'student_id' in columns or 'studentid' in columns
        is_raw_format = '姓名' in columns and '记录时间' in columns

        if not is_standard_format and not is_raw_format:
            total_failed += 1
            error_messages.append(f"文件[{filename}]格式不支持")
            error_messages.append("  支持的格式：")
            error_messages.append("  1. 原始导出格式：姓名、记录时间、状态")
            error_messages.append("  2. 标准数据库格式：student_id、attend_date、attend_type、check_time、status")
            continue

        file_success = 0
        file_failed = 0

        # 🔴 完全对齐本地脚本：维护上一行的日期和考勤类型
        last_attend_date = ""
        last_attend_type = ""

        for row_num, row_data in enumerate(data_list, start=2):
            try:
                # 统一列名处理（去除空格，转小写）
                row = {str(k).strip().lower(): v for k, v in row_data.items()}

                if is_standard_format:
                    # ==============================
                    # 处理标准数据库格式
                    # ==============================
                    student_id = str(row.get('student_id') or row.get('studentid') or '').strip()
                    attend_date = parse_date(row.get('attend_date') or row.get('attenddate'))
                    attend_type = str(row.get('attend_type') or row.get('attendtype') or '').strip()
                    check_time = parse_time(row.get('check_time') or row.get('checktime'), attend_date)
                    status = str(row.get('status') or '').strip()

                    # 标准格式必填字段验证
                    if not student_id:
                        raise ValueError("student_id不能为空")
                    if not attend_date:
                        raise ValueError("attend_date不能为空或格式错误")
                    if not attend_type:
                        raise ValueError("attend_type不能为空")
                    if not status:
                        raise ValueError("status不能为空")

                else:
                    # ==============================
                    # 处理原始导出格式（完全对齐本地脚本逻辑）
                    # ==============================
                    name = str(row_data.get('姓名', '')).strip()
                    record_time = str(row_data.get('记录时间', '')).strip()
                    status = str(row_data.get('状态', '')).strip()

                    # 原始格式必填字段验证
                    if not name:
                        raise ValueError("姓名不能为空")
                    if not status:
                        raise ValueError("状态不能为空")

                    # 🔴 完全对齐本地脚本：处理空时间和"——"
                    if record_time in ["", "——"]:
                        if not last_attend_date or not last_attend_type:
                            raise ValueError("第一行记录时间不能为空")

                        attend_date = last_attend_date
                        attend_type = last_attend_type
                        check_time = None

                    else:
                        # 🔴 完全对齐本地脚本：解析时间并自动判断考勤类型
                        try:
                            dt = pd.to_datetime(record_time)
                            attend_date = dt.strftime("%Y-%m-%d")
                            check_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                            hour = dt.hour
                            attend_type = "早自习" if hour < 12 else "晚自习"

                            # 更新上一行的值
                            last_attend_date = attend_date
                            last_attend_type = attend_type

                        except Exception as e:
                            if not last_attend_date or not last_attend_type:
                                raise ValueError(f"记录时间格式错误: {record_time}")

                            # 解析失败时使用上一行的值
                            attend_date = last_attend_date
                            attend_type = last_attend_type
                            check_time = None

                    # 通过姓名匹配student_id（转换为字符串）
                    if not name_to_id:
                        raise ValueError(f"班级[{student_class}]没有学生数据，无法匹配姓名")

                    if name not in name_to_id:
                        raise ValueError(f"姓名[{name}]在班级[{student_class}]中不存在")

                    student_id = name_to_id[name]

                # ==============================
                # 数据库ENUM类型严格验证
                # ==============================
                if attend_type not in ALLOWED_ATTEND_TYPES:
                    raise ValueError(f"考勤类型'{attend_type}'不合法，只能是：{', '.join(ALLOWED_ATTEND_TYPES)}")

                if status not in ALLOWED_STATUSES:
                    raise ValueError(f"状态'{status}'不合法，只能是：{', '.join(ALLOWED_STATUSES)}")

                # 构造最终插入参数（严格按照DAO层顺序和数据库类型）
                args = (
                    student_id,  # VARCHAR(20)
                    attend_date,  # DATE
                    attend_type,  # ENUM('早自习','晚自习')
                    check_time,  # DATETIME (允许NULL)
                    status,  # ENUM('正常','迟到','未到','请假')
                    recorder  # VARCHAR(20)
                )

                # 调用DAO层插入数据
                insert_one(args)
                file_success += 1

            except Exception as e:
                file_failed += 1
                error_messages.append(f"文件[{filename}]第{row_num}行错误: {str(e)}")

        total_success += file_success
        total_failed += file_failed

    # 构造返回消息
    msg_parts = []
    msg_parts.append(f"导入完成！班级：{student_class}")
    msg_parts.append(f"成功: {total_success}条，失败: {total_failed}条")

    if error_messages:
        msg_parts.append("\n错误详情：")
        for i, error in enumerate(error_messages[:20]):
            msg_parts.append(f"{i + 1}. {error}")

        if len(error_messages) > 20:
            msg_parts.append(f"...还有{len(error_messages) - 20}条错误未显示")

    return "\n".join(msg_parts)

def query_data(request):
    students = get_all_students()
    records = []
    n = l = t = a = 0
    qtype = ""
    if request.method == 'POST':
        qtype = request.form['query_type']
        if qtype == 'date':
            records = by_date(
                request.form.get('start_date'),
                request.form.get('end_date'),
                request.form.get('status_type')
            )
        elif qtype == 'name':
            records = by_student(
                request.form.get('student_id'),
                request.form.get('status_type')
            )
        for r in records:
            print(r)
            s = r['status']
            if s == '正常': n +=1
            elif s == '迟到': l +=1
            elif s == '请假': t +=1
            elif s == '未到': a +=1
    return {
        "students": students,
        "records": records,
        "normal": n, "late": l, "leave": t, "absent": a,
        "query_type": qtype
    }

def get_all_classes_service():
    return get_all_classes()
