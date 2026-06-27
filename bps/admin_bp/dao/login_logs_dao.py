from config import db


def get_login_logs_dao():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT * FROM login_log ORDER BY login_time DESC")
            # 获取查询结果
            data = cursor.fetchall()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")