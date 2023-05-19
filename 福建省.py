"""
CSDN: 抄代码抄错的小牛马
mailbox：yxhlhm2002@163.com
"""
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
# 修改编码方式
# 解决这个编码问题：UnicodeDecodeError: 'gbk' codec can't decode byte 0xac in position 186: illegal multibyte sequence
# 修改后再调用 execjs 就不报错 但每遇到编码问题都要手动添加修改一次

import time
import requests
import execjs

from userAgentPooL import userAgent
from ipPooL import IP

html_url = 'https://ggzyfw.fujian.gov.cn/business/list/'  # 主页面
data_api = 'https://ggzyfw.fujian.gov.cn/FwPortalApi/Trade/TradeInfo'  # 接口

ts = int(time.time() * 1000)
json_data = {
    "pageNo": 1,
    "pageSize": 20,  # 可修改
    "total": 0,
    "AREACODE": "",
    "M_PROJECT_TYPE": "",
    "KIND": "GCJS",
    "GGTYPE": "1",
    "PROTYPE": "",
    "timeType": "6",
    "BeginTime": "2022-11-19 00:00:00",
    "EndTime": "2023-05-19 23:59:59",
    "createTime": [],
    "ts": ts
}


# 调用JS代码 --> 标准MD5加密： portal-sign
def use_encrypt_sign():
    # 读取js文件
    with open('./portal-sign.js', encoding='utf-8') as f:
        js = f.read()

    # 通过compile命令转成一个js对象
    docjs = execjs.compile(js)
    # (调用函数, 参数1，参数2）
    encrypted_params = docjs.call('d', json_data)

    print('JS返回的portal-sign：', encrypted_params)

    return encrypted_params


# 携带加密的portal-sign进行请求 --> 返回加密后的数据：Data
def get_encryptdata(params):
    ua = userAgent.get_ua()
    ip = IP.get_ip()
    print(ip)
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "226",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "ggzyfw.fujian.gov.cn",
        "Origin": "https://ggzyfw.fujian.gov.cn",
        "portal-sign": params,
        "Referer": "https://ggzyfw.fujian.gov.cn/business/list/",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": ua
    }
    res = requests.post(url=data_api, headers=headers, json=json_data, proxies=ip)
    resp = res.json()['Data']

    # print(res.status_code)
    # print(res.json())
    # print(resp)

    return resp


# 传入接口返回的加密数据 --> AEC CBC 解密
def use_decrypt_data(resp):
    # 读取js文件
    with open('./decrypt_data.js', encoding='utf-8') as f:
        js = f.read()

    # 通过compile命令转成一个js对象
    docjs = execjs.compile(js)
    # (调用函数, 参数1，参数2）
    end_data = docjs.call('decrypt', resp, 'BE45D593014E4A4EB4449737660876CE', 'A8909931867B0425')

    print('===============解密后的数据===============')
    print(end_data)

    pass


if __name__ == '__main__':
    # 拿到请求体的：加密 portal-sign
    encrypted_params = use_encrypt_sign()
    # post 请求获取到加密后的数据
    resp = get_encryptdata(encrypted_params)
    # 进行数据解密
    use_decrypt_data(resp)
