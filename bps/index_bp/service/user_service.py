from bps.index_bp.dao.user_dao import get_user_data
from bps.index_bp.dao.user_dao import secret_key as user_secret_key
from bps.index_bp.dao.user_dao import update_status as user_update_status
from bps.index_bp.dao.user_dao import add_user as user_add_user
from bps.index_bp.dao.user_dao import update_signature
from bps.index_bp.dao.user_dao import update_username
from bps.index_bp.dao.user_dao import update_password


def get_user(username):
    return get_user_data(username)

# 处理得到的密钥数据
def secret_key():
    # 定义空列表来存储处理后的密钥
    key_list = []
    # 获得密钥
    secret_key = user_secret_key()
    # 遍历密钥列表
    for secret_key in secret_key:
        key = secret_key.get('key')
        key_list.append(key)
    return key_list

def update_status(passkey):
    user_update_status(passkey)

def add_user(username, password):
    user_add_user(username, password)

def updata_signature_service(username, signature):
    update_signature(username, signature)

def update_username_service(username, new_username):
    update_username(username, new_username)

def update_password_service(username, new_password):
    update_password(username, new_password)