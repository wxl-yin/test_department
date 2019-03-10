import os
import smtplib
import time
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from plugins import HTMLTestRunnerPlugins


def load_suites(suite_path, rule):
    """
    加载制定目录下的所有测试用例
    :param suite_path: 用例所在的路径
    :param rule: 用例文件的规则
    :return: 返回所有用例
    """
    suites = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(start_dir=suite_path,
                                                   pattern=rule,
                                                   top_level_dir=None
                                                   )
    # 添加所有用例
    suites.addTests(discover)
    # 返回
    return suites


def run_cases(suites, reports_path):
    """
    生成测试报告
    :param suites: 测试用例
    :param reports_path: 生成报告目录
    :return:
    """
    # 创建报告名
    reports_filename = time.strftime("%Y-%d-%m_%H_%M_%S_%p") + "_report.html"
    reports_filename_path = os.path.join(reports_path, reports_filename)
    with open(reports_filename_path, 'wb') as fp:
        runner = HTMLTestRunnerPlugins.HTMLTestRunner(title="自动化测试报告",
                                                      description="自动化测试用例详情",
                                                      retry=0,
                                                      verbosity=2,
                                                      stream=fp)
        # 执行
        runner.run(suites)

    # 返回报告路径
    return reports_filename_path


def send_mail(smtp_server, smtp_user, smtp_password, receive_user, report_filepath):
    # =================2. 准备参数========

    # 3. 写邮件

    multi_message = MIMEMultipart()
    multi_message['from'] = smtp_user
    multi_message['to'] = ";".join(receive_user)
    multi_message['subject'] = "自动化测试报告发送"

    # 处理邮件内容部分
    # 报告内容以文本形式发送
    with open(report_filepath, 'rb') as fp:
        file_attach_content = fp.read()
    message = MIMEText(_text=file_attach_content, _subtype="html", _charset="UTF-8")
    multi_message.attach(message)

    # 将报告已附件形式发送
    file_message = MIMEText(file_attach_content, _subtype='base64', _charset="UTF-8")
    # 内容类型 字节流
    file_message['Content-Type'] = "application/octet-stream"

    # 内容处理 附件形式 filename 只得是下载时候文件的名字
    report_name = os.path.basename(report_filepath)
    file_message['Content-Disposition'] = 'attachment;filename="{}"'.format(report_name)
    multi_message.attach(file_message)

    # ================== 4. 发送邮件=============
    """
    1. 创建smtplib对象
    2. 链接到邮箱服务器
    3. 登陆认证
    4. 发送邮件
    5. 关闭邮件
    """
    try:
        # 1. 创建smtplib对象
        smtp = smtplib.SMTP()
        # 2. 链接到邮箱服务器
        smtp.connect(host=smtp_server)
        # 3. 登陆认证
        smtp.login(smtp_user, smtp_password)
        # 4. 发送邮件
        smtp.sendmail(multi_message['from'], multi_message['to'], multi_message.as_string())
        # 5. 关闭邮件
        smtp.quit()
        print("发送邮件成功:{}".format(report_filepath))
    except smtplib.SMTPException as e:
        print("发送邮件失败:{}".format(e))


if __name__ == '__main__':
    # 1.获取当前项目的根目录
    base_dir = os.path.dirname(os.path.realpath(__file__))
    # print(base_dir)

    # 2. 加载项目中的所有测试用列
    # 用例所在目录
    suite_path = os.path.join(base_dir, 'test_suite')
    # print(suite_dir)
    # 加载制定规则的测试用例
    rule = "test*.py"
    suites = load_suites(suite_path, rule)

    # 3. 生成测试报告
    # 指明测试报告的目录
    reports_path = os.path.join(base_dir, 'report')
    # 生成报告
    report_filepath = run_cases(suites, reports_path)

    # 3. 将生成的测试报告通过邮件的形式发送

    # 获取最新的生成的报告
    # 通过邮件形式发送
    # 准备参数
    smtp_server = "smtp.163.com"
    smtp_user = "eric_cdycq@163.com"
    smtp_password = "admin123456"
    receive_user = ['yinqiang@itsource.cn']
    send_mail(smtp_server, smtp_user, smtp_password, receive_user, report_filepath)
    #更新

