from dbutils.pooled_db import PooledDB
import pymysql

def db():
    # 创建连接池
    pool = PooledDB(
        creator=pymysql,  # 使用 pymysql 作为数据库连接的创建者
        host='127.0.0.1',
        user='root',
        password='Xqy624070',
        database='qingyuweb',
        autocommit=False,  # 手动提交事务
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        mincached=2,  # 连接池中空闲连接的初始数量
        maxcached=4,  # 连接池中空闲连接的最大数量
        maxshared=3,  # 共享连接的最大数量
        maxconnections=6,  # 连接池允许的最大连接数
        blocking=True  # 连接池达到最大连接数时是否阻塞
    )
    return pool