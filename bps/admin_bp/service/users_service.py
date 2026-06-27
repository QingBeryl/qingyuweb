from bps.admin_bp.dao.users_dao import get_all_users_dao

# 调用dao层获取所有用户信息
def get_all_users_service():
    return get_all_users_dao()