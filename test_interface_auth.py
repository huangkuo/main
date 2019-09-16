# coding:utf-8
__author__ = 'kuoh'
# web端登录
import json
import requests
import unittest
import configparser
import os
import redis

def get_login_params(url):

    config_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = config_dir + '/config.ini'
    print(config_file_path)
    cf = configparser.ConfigParser()
    cf.read(config_file_path, encoding='utf-8')
    user =cf.get('web','user')
    password =cf.get('web','password')
    pd = cf.get('redis','redis_password')
    ip = cf.get('http','test_ip')
    # 获取验证码
    result = requests.get(url)
    pool = redis.ConnectionPool(host=ip,port=6379,password=pd,db=0)
    r = redis.StrictRedis(connection_pool=pool,decode_responses=False)
    # 获取uuid
    uuid = result.headers._store.get('uuid','UUID')[1]
    # 获取验证码
    captcha= str(r.get('captcha:login:'+ result.headers._store.get('uuid','UUID')[1])[1:5],encoding='utf8')
    # 模拟登陆
    return  {"username":user,"password":password,"captcha":captcha,"uuid":uuid}



class test_interface_auth(unittest.TestCase):


    def __init__(self, methodName = 'runTest' ):
        super(test_interface_auth, self).__init__(methodName)
        # 读取配置文件
        config_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = config_dir + '/config.ini'
        cf = configparser.ConfigParser()
        cf.read(config_file_path, encoding='utf-8')
        self.host = cf.get('http', 'test_host')
        self.ip = cf.get('http','test_ip')
        self.c_url = self.host + '/auth/captcha'
        self.l_url = self.host + '/auth/login'
        # print(self.url + '\n')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        print("测试接口/api/auth/login开始\n")

    @classmethod
    def tearDownClass(cls):
        print("测试接口/api/auth/login结束\n")

    def test_case_001(self):
        '''用例说明：正常登录场景'''
        print("测试正常登录场景开始\n")
        param = get_login_params(self.c_url)
        result = requests.post(self.l_url,json=param)
        r = json.loads(result.text)
        self.assertEqual(200, r['code'], msg='正常登录失败')
        print("测试正常登录场景结束\n")

    def test_case_002(self):
        '''用例说明：不输入用户名登录场景'''
        print("测试不输入用户名登录场景开始\n")
        param = get_login_params(self.c_url)
        param_new = {"username": "","password":param.get("password"),"captcha":param.get("captcha"),"uuid":param.get("uuid")}
        result = requests.post(self.l_url,json=param_new)
        r = json.loads(result.text)
        self.assertEqual(100203, r['code'], msg='不输入用户名登录场景验证失败')
        print("测试不输入用户名登录场景结束\n")

    def test_case_003(self):
        '''用例说明：不输入密码登录场景'''
        print("测试不输入密码登录场景开始\n")
        param = get_login_params(self.c_url)
        print(param.get("uuid"))
        param_new = {"username": param.get("username"),"password":"","captcha":param.get("captcha"),"uuid":param.get("uuid")}
        result = requests.post(self.l_url,json=param_new)
        r = json.loads(result.text)
        self.assertEqual(100304, r['code'], msg='不输入密码登录场景验证失败')
        print("测试不输入密码登录场景结束\n")

    def test_case_004(self):
        '''用例说明：不输入验证码登录场景'''
        print("测试不输入验证码登录场景开始\n")
        param = get_login_params(self.c_url)
        param_new = {"username": param.get("username"),"password":param.get("password"),"captcha":"","uuid":param.get("uuid")}
        result = requests.post(self.l_url,json=param_new)
        r = json.loads(result.text)
        self.assertEqual(100601, r['code'], msg='不输入验证码登录场景验证失败')
        print("测试不输入验证码登录场景结束\n")

    def test_case_005(self):
        '''用例说明：不输入uuid登录场景'''
        print("测试不输入验证码登录场景开始\n")
        param = get_login_params(self.c_url)
        param_new = {"username": param.get("username"),"password":param.get("password"),"captcha":param.get("captcha"),"uuid":""}
        result = requests.post(self.l_url,json=param_new)
        r = json.loads(result.text)
        self.assertEqual(100601, r['code'], msg='不输入uuid登录场景验证失败')
        print("测试不输入uuid登录场景结束\n")

    def login(self):
        param = get_login_params(self.c_url)
        result = requests.post(self.l_url,json=param)
        return result.headers.get('Set-Cookie').split(';')[0]

if __name__ == '__main__':
    print("测试接口app/member/login\n")
    unittest.main()
