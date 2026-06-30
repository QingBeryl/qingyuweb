# Python Flask Web项目部署教程
> 欢迎您使用本教程

本教程介绍在Linux系统下通过Gunicorn部署Python Flask项目、Nginx代理静态资源、数据库MySQL、Fail2ban保护服务器的详细教程，使用系统以及软件版本如下：
* Linux系统：CentOS-Stream-9
* Python解释器：3.11.9
* Gunicorn：26.0.0
* Nginx：1.30.2
* MySQL：8.0
* Fail2ban：2.5

## 一、准备工作
1. 在根目录创建**www**文件夹，在文件夹中分别创建data、static、*你的项目名称*文件夹，如图所示：
![alt text](/static/docs/docs1/images/image.png)
    * data：存放安装包等文件
    * static：存放Nginx管理的静态文件
    * *你的项目名称*：存放你的Flask项目代码文件（static静态文件除外）
2. 在data目录中上传或下载以下文件：
    * Python-3.11.9.tgz
    * nginx-1.30.2.tar.gz
    * mysql84-community-release-el9-1.noarch.rpm
3. 在static中上传项目所需的静态文件，如没有则忽略
4. 在*你的项目名称*文件夹中上传你的Flask项目代码文件（static静态文件除外）

## 二、安装python解释器

### 1.安装依赖
直接运行以下命令：
```
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make
```
运行结果如图所示； 
![alt text](/static/docs/docs1/images/image-1.png)
---
### 2.解压
进入data目录解压 Python-3.11.9.tgz 文件：
```
cd data
tar -zxvf Python-3.11.9.tgz
```  
运行结果如图：
![alt text](/static/docs/docs1/images/image-2.png)
---
### 3.配置
进入 Python-3.11.9 目录：
```
cd Python-3.11.9
```
可以看到有 configure 文件，如图；
![alt text](/static/docs/docs1/images/image-3.png)  

执行以下命令：  

```
./configure --prefix=/opt/python311 --enable-optimizations
```  

### 4.编译&安装
执行以下命令：
```
make & make install
```
运行结果如图：
![alt text](/static/docs/docs1/images/image-4.png)
### 5.创建软连接
```
ln -s /opt/python311/bin/python3.11 /usr/local/bin/python311
```
### 6.配置环境变量
执行
```
vi ~/.bash_profile
```
在文件中加上以下内容：
```
export PYTHON_HOME=/opt/python311
export PATH=$PYTHON_HOME/bin:$PATH
```
### 7.执行`source ~/.bash_profile`命令使配置生效。执行`echo`命令，查看是否配置成功

## 三、虚拟环境的创建及使用

### 1.创建虚拟环境
先进入项目文件夹，执行：
```
cd /
cd www/项目文件夹
```
创建虚拟环境，执行：
```
python3.11 -m venv venv
```
无报错即为成功，多出一个venv文件夹，如图：               
![alt text](/static/docs/docs1/images/image-5.png)
### 2.进入虚拟环境
在项目文件夹执行：
```
source venv/bin/activate
```
结果如图，显示venv即为成功：
![alt text](/static/docs/docs1/images/image-6.png)
### 3.退出环境
执行，venv消失即为成功
```
deactivate
```
如图：
![alt text](/static/docs/docs1/images/image-7.png)


## 四、gunicorn配置及启动
### 1.配置文件
将以上内容添加到gunicorn.conf.py文件中，如没有这在项目文件夹新建一个
```
# 项目目录
chdir = '/www/qingyuweb'

# 指定进程数
workers = 4

# 指定每个进程开启的线程数
threads = 2

#启动用户
user = 'root'

# 后台运行
daemon = True  # 后台运行

# 启动模式
worker_class = 'sync'

# 绑定的ip与端口
bind = '0.0.0.0:8000' 

# 设置进程文件目录（用于停止服务和重启服务，请勿删除）
pidfile = '/www/qingyuweb/logs/gunicorn.pid'

# 设置访问日志和错误信息日志路径
accesslog = '/www/qingyuweb/logs/gunicorn_acess.log'
errorlog = '/www/qingyuweb/logs/gunicorn_error.log'

# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
# debug:调试级别，记录的信息最多；
# info:普通级别；
# warning:警告消息；
# error:错误消息；
# critical:严重错误消息；
loglevel = 'info' 

# 自定义设置项请写到该处
# 最好以上面相同的格式 <注释 + 换行 + key = value> 进行书写， 
# PS: gunicorn 的配置文件是python扩展形式，即".py"文件，需要注意遵从python语法，
# 如：loglevel的等级是字符串作为配置的，需要用引号包裹起来
```
### 2.python第三方库依赖安装（包括gunicorn）
进入虚拟环境运行：
```
pip install -r requirements.txt
```
需确保项目文件夹存在requirements.txt文件，如图：
![alt text](/static/docs/docs1/images/image-8.png)
### 3.启动命令（app代表项目入口文件名称，如不同清修改）
```
python -m gunicorn app:app
```
无报错即为成功，如图：
![alt text](/static/docs/docs1/images/image-12.png)

## 五、nginx安装/配置/启动
### 1.解压文件
先进入data文件夹
```
cd data
```
运行命令解压 nginx-1.30.2.tar.gz 文件
```
tar -zxvf nginx-1.30.2.tar.gz
```
运行结果如图：
![alt text](/static/docs/docs1/images/image-9.png)
### 2.配置 
先进入 nginx-1.30.2 文件夹
可以看到有一个 configure 文件：
![alt text](/static/docs/docs1/images/image-10.png)
运行以下命令：
```
./configure --prefix=/opt/nginx
```
### 4.编译&安装
执行以下命令：
```
make & make install
```
### 5.启动 nginx
进入 nginx 安装目录，执行：
```
cd /opt/nginx/sbin/
```
可以看到一个 nginx 文件，如图：                             
![alt text](/static/docs/docs1/images/image-11.png)  

运行启动命令：
```
./nginx
```
无报错即为成功

### 6.配置文件（实现反向代理和动静分离）
运行以下命令，进入 nginx 配置文件夹
```
cd /opt/nginx/conf
```
在 nginx.conf 文件中的server部分加上一下内容：
```
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_redirect off;
}

location ~ .*\.(js|css|png|jpg|jpeg|gif|ico|svg|mp4|m3u8|ttf|woff)$
{
    root /www/;
    expires      30h;
}
```

### 7.重新加载配置文件
```
./nginx -s reload
```
### 8.其它命令（都需在 nginx 的sbin目录下运行，否则会报错）
停止
```
./nginx -s stop
```
安全退出
```
./nginx -s quit
```
## 六、mysql安装
### 1.查询已安装的 MariaDB 相关软件包
```
rpm -qa|grep mariadb
```
如图即为没有，跳过步骤2：                    
![alt text](/static/docs/docs1/images/image-13.png)  

### 2.删除MariaDB
```
rpm -e mariadb-libs-5.5.64-1.el7.x86_64 --nodeps
```
### 3.安装网络安装工具wget
```
yum -y install wget
```
如图即为成功：               
![alt text](/static/docs/docs1/images/image-14.png)  


### 4.安装配置文件
先进入data目录：
```
cd /
cd www/data
```
运行：
```
yum -y install mysql84-community-release-el9-1.noarch.rpm
```
结果如图所示：
![alt text](/static/docs/docs1/images/image-15.png)  

### 5.安装mysql
运行：
```
yum -y install mysql-community-server
```
运行结果如图所示：            
![alt text](/static/docs/docs1/images/image-16.png)

### 6.启动mysql
运行：
```
systemctl start mysqld
```
检查 mysql 运行状态：
```
systemctl status mysqld
```
正常如图所示：             
![alt text](/static/docs/docs1/images/image-17.png)  

### 7.查看临时密码
```
grep 'temporary password' /var/log/mysqld.log
```
密码如图：                       
![alt text](/static/docs/docs1/images/image-18.png)  

### 8.修改初始密码
先登录 mysql，运行并输入临时密码：
```
mysql -uroot -p
```
如图：                   
![alt text](/static/docs/docs1/images/image-19.png)

运行下列代码修改密码：
```
ALTER USER 'root'@'localhost' IDENTIFIED BY '密码';
```
运行结果如图：                    
![alt text](/static/docs/docs1/images/image-20.png)  

### 9.mysql配置文件
编辑/ets/my.conf文件，加上以下内容（性能好的服务器请忽略）：
```
max_connections=10
wait_timeout=30
interactive_timeout=30

innodb_buffer_pool_size=128M
innodb_log_file_size=128M
innodb_log_buffer_size=4M

sort_buffer_size=32K
read_buffer_size=32K
read_rnd_buffer_size=32K
join_buffer_size=32K

tmp_table_size=16M
max_heap_table_size=16M

performance_schema=OFF
default-storage-engine=innodb

innodb_read_io_threads=1
innodb_write_io_threads=1
innodb_buffer_pool_instances=1
```


## 七、fail2ban
### 1.安装依赖
```
sudo dnf install -y epel-release
```
运行结果如图所示：              
![alt text](/static/docs/docs1/images/image-21.png)  

### 2.安装 fail2ban 以及防火墙依赖
```
yum install -y fail2ban fail2ban-firewalld
```
运行结果如图所示：                
![alt text](/static/docs/docs1/images/image-22.png)  

### 3.启动
```
sudo systemctl start fail2ban
```
无报错即为启动成功：                           
![alt text](/static/docs/docs1/images/image-23.png)  

### 4.备份配置文件
执行：
```
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```
后续配置文件的修改一律在 jail.local 文件中，或在其他新建文件中，绝对禁止修改 jail.conf 中的内容

### 5.SSH防御 防止暴力破解
#### 删除默认文件
```
rm -rf /etc/fail2ban/jail.d/*
```
#### 编辑ssh策略
```
vi /etc/fail2ban/jail.d/sshd.local
```
在文件中添加以下内容：
```
[sshd]

enabled = true
mode = normal
backend = systemd
```
#### 重启服务
```
systemctl restart fail2ban
```
#### 查看封锁列表
```
fail2ban-client status
```
#### 查看SSH封锁情况
```
fail2ban-client status sshd
```
### 6.创建网站拦截规则
#### 编辑 nginx 网址策略
```
vi /etc/fail2ban/jail.d/nginx.local
```
在文件中添加以下内容：
```
[nginx-http-auth]

enabled = true

mode = fallback

port = http,https

logpath = /opt/nginx/logs/access.log

[nginx-limit-req]

enabled = true

port    = http,https

logpath = /opt/nginx/logs/access.log

[nginx-botsearch]

enabled = true

port     = http,https

logpath = /opt/nginx/logs/access.log

[nginx-bad-request]

enabled = true

port    = http,https

logpath = /opt/nginx/logs/access.log

[php-url-fopen]

enabled = true

port    = http,https

logpath = /opt/nginx/logs/access.log
```
#### 查看nginx封锁情况
```
fail2ban-client status nginx-http-auth
```
#### 查看总日志
```
tail -f /var/log/fail2ban.log
```

## 八、其它命令
### 检查防火墙状态
```
systemctl status firewalld
```
### 启动/停止防火墙
```
systemctl start firewalld
systemctl stop firewalld
```
### 开启/停止端口
```
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --zone=public --remove-port=8080/tcp --permanent
```
### 重载防火墙
```
firewall-cmd --reload
```
### 查看已开发端口
```
firewall-cmd --list-ports
```
### 查看端口占用
```
sudo ss -tulnp | grep :8000
```
### 创建用户
```
useradd zhangsan
passwd zhangsan
```
### 创建用户，不可登录
```
useradd -M -s /sbin/nologin www
```

参数解释
* -M  不创建家目录
* -s /sbin/nologin  禁止登录服务器

### 授与权限
```
chown -R www:www /www/qingyuweb
```
### 资源监控脚本
编辑脚本
```
vi /usr/local/bin/server_monitor.sh
```
在文件中添加以下内容：
```
#!/bin/bash

# 所有记录写入同一个日志文件
LOG_FILE="/var/log/server_monitor.log"

# 分隔线
divider() {
    echo "========================================================================" >> "${LOG_FILE}"
}

# 主监控逻辑
monitor() {
    local NOW_TIME="$(date '+%Y-%m-%d %H:%M:%S')"
    divider
    echo "监控时间: ${NOW_TIME}" >> "${LOG_FILE}"
    echo "========== 服务器资源监控 ==========" >> "${LOG_FILE}"

    # 1. 系统负载 & CPU
    echo -e "\n【系统负载 & CPU】" >> "${LOG_FILE}"
    echo "1/5/15分钟负载: $(uptime | awk -F'load average:' '{print $2}')" >> "${LOG_FILE}"
    top -bn1 | grep '^%Cpu' | awk '{printf "CPU 使用: 用户 %.1f%%, 系统 %.1f%%, 空闲 %.1f%%\n", $2, $4, $8}' >> "${LOG_FILE}"

    # 2. 内存
    echo -e "\n【内存使用】" >> "${LOG_FILE}"
    free -h | awk 'NR==2{print "内存: 总"$2", 已用"$3", 空闲"$4", 缓存"$6}' >> "${LOG_FILE}"

    # 3. 磁盘
    echo -e "\n【磁盘使用】" >> "${LOG_FILE}"
    df -h | grep -E '^/dev/' | grep -v 'tmpfs' | awk '{print $1 " 总"$2 ", 已用"$3 ", 剩余"$4 ", 使用率"$5}' >> "${LOG_FILE}"

    # 4. 网络
    echo -e "\n【网络状态】" >> "${LOG_FILE}"
    echo "TCP 总连接: $(ss -t | wc -l)" >> "${LOG_FILE}"
    echo "已建立连接: $(ss -t state established | wc -l)" >> "${LOG_FILE}"
    echo "等待连接: $(ss -t state time-wait | wc -l)" >> "${LOG_FILE}"

    # 5. fail2ban
    echo -e "\n【Fail2Ban 状态】" >> "${LOG_FILE}"
    if pgrep -f fail2ban > /dev/null; then
        echo "运行状态: 正在运行" >> "${LOG_FILE}"
        echo "累计封禁IP数: $(fail2ban-client status 2>/dev/null | grep 'Total banned' | awk '{print $4}')" >> "${LOG_FILE}"
        echo "SSH封禁列表: $(fail2ban-client status sshd 2>/dev/null | grep 'Banned IP list' | cut -d: -f2 | xargs)" >> "${LOG_FILE}"
    else
        echo "运行状态: 未运行" >> "${LOG_FILE}"
    fi

    # ==================== Nginx 状态（万能检测，不依赖路径）====================
    echo -e "\n【Nginx 状态】" >> "${LOG_FILE}"
    if pgrep -f nginx > /dev/null; then
        PID=$(pgrep -f nginx | head -1)
        NUM=$(pgrep -f nginx | wc -l)
        CPU=$(ps -p $PID -o pcpu= | xargs)
        MEM=$(ps -p $PID -o pmem= | xargs)
        echo "运行状态: 正在运行" >> "${LOG_FILE}"
        echo "主进程PID: $PID" >> "${LOG_FILE}"
        echo "进程数量: $NUM" >> "${LOG_FILE}"
        echo "占用资源: CPU $CPU% 内存 $MEM%" >> "${LOG_FILE}"
    else
        echo "运行状态: 未运行" >> "${LOG_FILE}"
    fi

    # ==================== MySQL 状态（万能检测，不依赖路径）====================
    echo -e "\n【MySQL 状态】" >> "${LOG_FILE}"
    if pgrep -f mysqld > /dev/null || pgrep -f mysql > /dev/null; then
        PID=$(pgrep -f mysqld 2>/dev/null || pgrep -f mysql 2>/dev/null | head -1)
        NUM=$(pgrep -f mysqld 2>/dev/null || pgrep -f mysql 2>/dev/null | wc -l)
        CPU=$(ps -p $PID -o pcpu= | xargs)
        MEM=$(ps -p $PID -o pmem= | xargs)
        echo "运行状态: 正在运行" >> "${LOG_FILE}"
        echo "主进程PID: $PID" >> "${LOG_FILE}"
        echo "进程数量: $NUM" >> "${LOG_FILE}"
        echo "占用资源: CPU $CPU% 内存 $MEM%" >> "${LOG_FILE}"
    else
        echo "运行状态: 未运行" >> "${LOG_FILE}"
    fi

    # ==================== Gunicorn 状态（万能检测，不依赖路径）====================
    echo -e "\n【Gunicorn 状态】" >> "${LOG_FILE}"
    if pgrep -f gunicorn > /dev/null; then
        PID=$(pgrep -f gunicorn | head -1)
        NUM=$(pgrep -f gunicorn | wc -l)
        CPU=$(ps -p $PID -o pcpu= | xargs)
        MEM=$(ps -p $PID -o pmem= | xargs)
        echo "运行状态: 正在运行" >> "${LOG_FILE}"
        echo "主进程PID: $PID" >> "${LOG_FILE}"
        echo "进程数量: $NUM" >> "${LOG_FILE}"
        echo "占用资源: CPU $CPU% 内存 $MEM%" >> "${LOG_FILE}"
    else
        echo "运行状态: 未运行" >> "${LOG_FILE}"
    fi

    echo -e "\n" >> "${LOG_FILE}"
    divider
}

# 执行监控
monitor
```
### 授予执行权限
```
chmod +x /usr/local/bin/server_monitor.sh
```
### 设置定时执行
```
crontab -e
*/5 * * * * /usr/local/bin/server_monitor.sh
```
### 内存查看/释放
```
free -h
sync && echo 3 > /proc/sys/vm/drop_caches
```
