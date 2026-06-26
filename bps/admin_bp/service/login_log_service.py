from datetime import datetime
from bps.admin_bp.dao.login_log_dao import insert_login_log_dao, get_user_count_dao, get_user_secret_count_dao, get_login_log_count_dao, get_logs_dao, get_all_users_dao

# 记录用户登录信息
def insert_login_log_service(user_id, username, clientip, device):
    insert_login_log_dao(user_id, username, clientip, device, datetime.now())

def get_user_count_service():
    return get_user_count_dao().get('count')

def get_user_secret_count_service():
    return get_user_secret_count_dao().get('count')

def get_login_log_count_service():
    return get_login_log_count_dao().get('count')

def get_logs_service():
    return get_logs_dao()

def get_all_users_service():
    return get_all_users_dao()