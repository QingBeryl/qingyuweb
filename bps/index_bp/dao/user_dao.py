from config import db

def get_user_data(username):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT id, username, password, signature FROM users WHERE username=%s", (username,))
            # 获取查询结果
            user = cursor.fetchone()
            return user
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

# 查询可以秘钥
def secret_key():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT id, `key`, status FROM secret WHERE status='0'")
            # 获取查询结果
            key = cursor.fetchall()
            return key
    except Exception as e:
        print(f"查询数据时出现错误: {e}")


# 更改密钥状态
def update_status(passkey):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("UPDATE secret SET status='1' WHERE `key`=%s ", (passkey,))
            conn.commit()
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def add_user(username, password):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            # 获取查询结果
            user = cursor.fetchone()
            return user
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def update_signature(username, signature):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("UPDATE users SET signature=%s WHERE username=%s", (signature, username,))
            conn.commit()
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def update_username(username, new_username):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("UPDATE users SET username=%s WHERE username=%s", (new_username, username,))
            conn.commit()
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def update_password(username, new_password):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username,))
            conn.commit()
    except Exception as e:
        print(f"查询数据时出现错误: {e}")