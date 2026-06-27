from config import db

# 记录用户登录信息
def insert_login_log_dao(user_id, username, clientip, device, datetime):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("""INSERT INTO login_log (user_id, username, ip_address, device_info, login_time)
                           VALUES (%s, %s, %s, %s, %s)""", (user_id, username, clientip, device, datetime))
            conn.commit()
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

# 获取用户数量
def get_user_count_dao():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT COUNT(*) as count FROM users")
            # 获取查询结果
            data = cursor.fetchone()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

# 获取秘钥数量
def get_user_secret_count_dao():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT COUNT(*) as count FROM secret WHERE status = '0'")
            # 获取查询结果
            data = cursor.fetchone()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

# 获取登录日志数量
def get_login_log_count_dao():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT COUNT(*) as count FROM login_log")
            # 获取查询结果
            data = cursor.fetchone()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

# 获取最近日志信息
def get_recent_logs_dao():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT * FROM login_log ORDER BY login_time DESC LIMIT 10")
            # 获取查询结果
            data = cursor.fetchall()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")




