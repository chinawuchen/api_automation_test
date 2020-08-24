import smtplib
from email.mime.text import MIMEText


class SendEmail(object):

    def __init__(self):
        self.email_host = "smtp.163.com"
        self.send_user = "13045899811@163.com"
        self.password = "ESPPZNIOAKRJJWNK"

    def send_mail(self, user_list, sub, content):
        user = "wuchen" + "<" + self.send_user + ">"
        # 构建邮件
        message = MIMEText(content, _subtype="plain", _charset="utf-8")
        # 主题
        message["Subject"] = sub
        # 发件人
        message["From"] = user
        # 收件人
        message["To"] = ";".join(user_list)
        # 创建SMTP服务，连接163邮件服务器
        server = smtplib.SMTP()
        server.connect(self.email_host)
        # 登录发件人邮箱
        server.login(self.send_user, self.password)
        # 发送邮件,然后关闭服务
        server.sendmail(user, user_list, message.as_string())
        server.close()

    def send_main(self, pass_list, fail_list):
        pass_num = float(len(pass_list))
        fail_num = float(len(fail_list))
        count_num = pass_num + fail_num
        # 成功率
        pass_result = "%.2f%%" % (pass_num/count_num*100)
        # 失败率
        fail_result = "%.2f%%" % (fail_num/count_num*100)
        user_list = ["1102055693@qq.com"]
        sub = "api自动化"
        content = "此次一共运行接口%s个,通过%s个,失败%s个,通过率为%s,失败率为%s"%(count_num, pass_num, fail_num, pass_result, fail_result)
        self.send_mail(user_list, sub, content)

if __name__ == "__main__":
    sen = SendEmail()
    sen.send_main([1,2],[4,5,6])


