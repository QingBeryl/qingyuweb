# --------------------------
# bcrypt核心加密/验证函数
# --------------------------
import bcrypt


def bcrypt_hash(password: str, rounds: int = 13) -> str:
    """
    使用bcrypt加密密码
    :param password: 待加密的密码字符串（前端传来的SHA-256哈希值）
    :param rounds: 工作因子，值越大越安全，计算时间越长
                   推荐值：前端10-11，后端12-14（加密一次约100-300ms）
    :return: 包含盐值的bcrypt哈希字符串
    """
    # bcrypt要求输入为bytes类型
    password_bytes = password.encode('utf-8')
    # 生成盐值并加密
    salt = bcrypt.gensalt(rounds=rounds)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # 转换为字符串返回
    return hashed_bytes.decode('utf-8')

def bcrypt_verify(password: str, hashed_password: str) -> bool:
    """
    验证密码是否匹配
    :param password: 用户输入的密码（前端传来的SHA-256哈希值）
    :param hashed_password: 数据库中存储的bcrypt哈希字符串
    :return: 匹配返回True，不匹配返回False
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)