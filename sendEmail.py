# coding:utf-8
__author__ = 'fxh'

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import os
import configparser



class MyEmail:
    def __init__(self):
        # 读取数据库配置文件
        #还是用绝对路径的好，相对路径在runner机执行时找不到这个配置文件
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = self.dir_path + '/config.ini'
        '''
        if os.path.exists(config_file_path):
            print("OK,文件存在")
        else:
            print("NO,文件不存在")
        '''
        cf = configparser.ConfigParser()
        cf.read(self.config_file_path, encoding='utf-8')

        self.host = cf.get('email', 'mail_host')    # 邮件发送服务器'smtp.exmail.qq.com'
        self.port = cf.get('email', 'mail_port')    # 465
        self.user = cf.get('email', 'mail_user')    # 邮箱账号
        self.password = cf.get('email', 'mail_pass')    # 邮箱密码
        self.sender = cf.get('email', 'sender')     # 发件人
        self.to = cf.get('email', 'receiver')       # 收件人
        self.cc = cf.get('email', 'cc')             # 邮件抄送人

        if self.cc == '':
            self.receiver = self.to
        elif self.to == '':
            self.receiver = self.cc
        else:
            self.receiver = self.to + ';' + self.cc

        self.subject = cf.get('email', 'subject')   # 邮件标题
        self.report_file = ''
        self.content = cf.get('email', 'content')   # 邮件正文

        self.message = MIMEMultipart()
        self.message['From'] = self.sender
        self.message['To'] = self.to
        self.message['Cc'] = self.cc
        self.message['Subject'] = self.subject
        self.message['Date'] = formatdate()
        pass

    def get_attachment(self):
        self.get_attach_file_name()
        # 附件内容加入邮件正文
        with open(self.report_file, 'r', encoding='utf-8') as f:
            x = f.read()
            self.content += x
        # 构造附件
        with open(self.report_file, 'rb') as f:
            attachment = MIMEText(f.read(), "base64", "utf-8")

        attachment["Content-Type"] = "application/octet-stream"
        filename = os.path.basename(self.report_file)
        # 附件名称为中文时的写法
        attachment.add_header("Content-Disposition", "attachment", filename=("gbk", "", filename))
        # 附件名称非中文时的写法
        # att["Content-Disposition"] = 'attachment; filename="test.html")'

        self.message.attach(attachment)
        return self

    def get_attach_file_name(self, file_dir=None):
        if file_dir:
            report_dir = file_dir
        else:
            report_dir = self.dir_path + '/test_reports'

        if report_dir[-1] != '\\' and report_dir[-1] != '/':
            report_dir += "/"

        lists = os.listdir(report_dir)
        lists.sort(key=lambda fn: os.path.getctime(report_dir + fn))  # 按时间排序
        print(lists)
        # 先找到想要发送邮件的报告文件
        self.report_file = os.path.join(report_dir, lists[-1])
        return self.report_file

    def send_email(self):
        self.message.attach(MIMEText(self.content, 'html', 'utf-8'))
        if self.receiver == '':
            print("收件人为空，不发送邮件。请检查收件人和抄送人配置是否正确")
            return
        # 发送邮件
        try:
            smtp = smtplib.SMTP_SSL(self.host, port=self.port)
            smtp.login(self.user, self.password)
            # 发送给多人、同时抄送给多人，发送人和抄送人放在同一个列表中
            smtp.sendmail(self.sender, self.receiver.split(";"), self.message.as_string())
        except smtplib.SMTPException as e:
            print('error:', e)
        pass


if __name__ == '__main__':
    my = MyEmail()
    my.get_attachment()
    my.send_email()

