from config import db

def get_all_students():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db().connection()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT * FROM attendance_students ORDER BY student_id")
            # 获取查询结果
            data = cursor.fetchall()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")
    finally:
        # 关闭游标和连接，连接会返回到连接池
        if conn:
            conn.close()