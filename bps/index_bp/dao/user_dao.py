from config import db

def get_user_data(username):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db().connection()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT id, username, password FROM users WHERE username=%s", (username,))
            # 获取查询结果
            user = cursor.fetchone()
            return user
    except Exception as e:
        print(f"查询数据时出现错误: {e}")
    finally:
        # 关闭游标和连接，连接会返回到连接池
        if conn:
            conn.close()

# 查询可以秘钥
def secret_key():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db().connection()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT id, `key`, status FROM secret WHERE status='0'")
            # 获取查询结果
            key = cursor.fetchall()
            return key
    except Exception as e:
        print(f"查询数据时出现错误: {e}")
    finally:
        # 关闭游标和连接，连接会返回到连接池
        if conn:
            conn.close()


# 更改密钥状态
def update_status(passkey):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db().connection()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("UPDATE secret SET status='1' WHERE `key`=%s ", (passkey,))
            conn.commit()
    except Exception as e:
        print(f"查询数据时出现错误: {e}")
    finally:
        # 关闭游标和连接，连接会返回到连接池
        if conn:
            conn.close()

def add_user(username, password):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db().connection()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            # 获取查询结果
            user = cursor.fetchone()
            return user
    except Exception as e:
        print(f"查询数据时出现错误: {e}")
    finally:
        # 关闭游标和连接，连接会返回到连接池
        if conn:
            conn.close()