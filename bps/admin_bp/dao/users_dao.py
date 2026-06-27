from config import db

# 获取所有用户信息
def get_all_users_dao():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT id, username, signature FROM users")
            # 获取查询结果
            data = cursor.fetchall()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def get_user_by_id_dao(id):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT id, username, password, signature FROM users WHERE id=%s", (id,))
            # 获取查询结果
            user = cursor.fetchone()
            return user
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def update_user_by_id(id, username, signature, password):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("UPDATE users SET username=%s, signature=%s, password=%s WHERE id=%s", (username, signature, password, id))
            conn.commit()
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

