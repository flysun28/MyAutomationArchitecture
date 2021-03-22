#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:08
# comment:
import os
# 切割路径，得到顶级目录路径（windows目录切换linux）
project_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
project_path.replace('\\', '/')

# 环境切换
environment_path = os.path.join(project_path, 'config/', 'environment.ini')
# 国内数据库
mysql_in_path = os.path.join(project_path, 'config/', 'mysql_in.ini')
# 公钥
public_key_path = os.path.join(project_path, 'config/', 'public.pem')
# 加密json传输rsa公钥
encjson_rsa_public_key_path = os.path.join(project_path, 'config/', 'encjson_rsa_public.pem')
# 签名拼接字符串
join_sign_path = os.path.join(project_path, 'config/', 'join_sign_key.ini')
# 用例执行
do_case_path = os.path.join(project_path, 'config/', 'do_case.ini')
# 密钥
key_path = os.path.join(project_path, 'config/', 'key.ini')