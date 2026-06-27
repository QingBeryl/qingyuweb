from bps.admin_bp.dao.key_dao import get_all_keys_dao, add_key_dao
from bps.index_bp.utils.secret_util import generate_secure_password

def get_all_keys_service():
    return get_all_keys_dao()

def add_key_service():
    add_key_dao(generate_secure_password())