from config import db

def get_all_keys_dao():
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("SELECT * FROM secret ORDER BY id DESC")
            # 获取查询结果
            data = cursor.fetchall()
            return data
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

def add_key_dao(key):
    conn = None
    try:
        # 从连接池中获取一个连接
        conn = db()
        with conn.cursor() as cursor:
            # 执行查询语句
            cursor.execute("INSERT INTO secret (`key`, status) VALUES (%s, %s)", (key, '0'))
            conn.commit()
            # 获取查询结果
            user = cursor.fetchone()
            return user
    except Exception as e:
        print(f"查询数据时出现错误: {e}")

