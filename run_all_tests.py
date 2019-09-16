# coding:utf-8
__author__ = 'fxh'
import unittest
import os
import HTMLTestRunner
import datetime
from sendEmail import MyEmail
#import db_data_init

dir_path = os.path.dirname(os.path.abspath(__file__))
discover = unittest.defaultTestLoader.discover(dir_path, 'test_interface_*.py')
#db_data_init.db_data_init()
if __name__ == '__main__':
    # runner = unittest.TextTestRunner()
    # runner.run(discover)

    # 如果不存在报告目录，则创建测试报告目录
    if not os.path.exists(dir_path + '/test_reports'):
        os.mkdir(dir_path + '/test_reports')

    fr = open(dir_path + '/test_reports/Test_Report_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.html', 'wb')
    report = HTMLTestRunner.HTMLTestRunner(stream=fr, title='MaaS_Charge接口测试报告', description='测试报告详情')
    report.run(discover)

    my = MyEmail()
    my.get_attachment().send_email()
