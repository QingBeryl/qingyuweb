import string
import secrets

def get_client_ip(request):
    """获取客户端真实IP"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def get_device_info(request):
    """获取设备信息"""
    return request.user_agent.string[:500]