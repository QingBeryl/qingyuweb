from datetime import datetime
from bps.admin_bp.dao.dashboard_dao import insert_login_log_dao, get_user_count_dao, get_user_secret_count_dao, get_login_log_count_dao, get_recent_logs_dao

# 调用dao层记录用户登录信息
def insert_login_log_service(user_id, username, clientip, device):
    insert_login_log_dao(user_id, username, clientip, device, datetime.now())

# 调用dao层获取用户数量
def get_user_count_service():
    return get_user_count_dao().get('count')

# 调用dao层获取秘钥数量
def get_user_secret_count_service():
    return get_user_secret_count_dao().get('count')

# 调用dao层获取所以登录数量
def get_login_log_count_service():
    return get_login_log_count_dao().get('count')

# 调用dao层获取最近登录信息
def get_recent_logs_service():
    return get_recent_logs_dao()

