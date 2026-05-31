from config import db

# 定义获取所有记录的函数
def get_all_records():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT a.*,s.name FROM attendance a LEFT JOIN attendance_students s ON a.student_id=s.student_id ORDER BY a.id DESC")
            # 获取查询结果
            data = cursor.fetchall()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def insert_one(args):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute('''INSERT INTO attendance(student_id,attend_date,attend_type,check_time,status,recorder)
                 VALUES (%s,%s,%s,%s,%s,%s)''', args)
            conn.commit()
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def by_date(start, end, status):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            sql = "SELECT a.*,s.name FROM attendance a LEFT JOIN attendance_students s ON a.student_id=s.student_id WHERE 1=1"
            args = []
            if start:
                sql += " AND a.attend_date>=%s"
                args.append(start)
            if end:
                sql += " AND a.attend_date<=%s"
                args.append(end)
            if status:
                sql += " AND a.status=%s"
                args.append(status)
            cursor.execute(sql, args)
            # 获取查询结果
            data = cursor.fetchall()
            print(data)
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def by_student(sid, status):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            sql = "SELECT a.*,s.name FROM attendance a LEFT JOIN attendance_students s ON a.student_id=s.student_id WHERE a.student_id=%s"
            args = [sid]
            if status:
                sql += " AND a.status=%s"
                args.append(status)
            cursor.execute(sql, args)
            # 获取查询结果
            data = cursor.fetchall()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

