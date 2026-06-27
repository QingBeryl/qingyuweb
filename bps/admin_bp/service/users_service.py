from bps.admin_bp.dao.users_dao import get_all_users_dao, get_user_by_id_dao, update_user_by_id

# 调用dao层获取所有用户信息
def get_all_users_service():
    return get_all_users_dao()

def get_user_by_id(id):
    return get_user_by_id_dao(id)

def updata_user_by_id_service(username, signature, password, id):
    update_user_by_id(username, signature, password, id)
