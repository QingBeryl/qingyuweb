import secrets
import string

# 1. 安全生成16位密码（字母+数字+特殊字符）
def generate_secure_password(length=255):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# 测试
print(generate_secure_password())