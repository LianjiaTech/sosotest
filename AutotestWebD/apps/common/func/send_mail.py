from AutotestWebD.settings import EMAIL_SENDER,EMAIL_PASSWORD,EMAIL_SERVER,EMAIL_USERNAME
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
import os
import email.encoders
import time
import traceback
import re


def send_mail(email_list, subject, email_text, filepath="", sub_type="text"):
    try:
        # 发送email
        receiver = list(set(email_list.split(';')))
        sender = EMAIL_SENDER
        smtpserver = EMAIL_SERVER
        username = EMAIL_USERNAME
        password = EMAIL_PASSWORD

        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        msg = MIMEMultipart()  #
        if sub_type == "text":
            text_msg = MIMEText(email_text, 'plain', 'utf-8')  # 文本格式
        elif sub_type == "html":
            text_msg = MIMEText(email_text, _subtype='html', _charset='utf-8')  # html格式
        else:
            text_msg = MIMEText(email_text, 'plain', 'utf-8')  # 文本格式
        msg.attach(text_msg)
        msg['From'] = sender
        msg['To'] = ";".join(receiver)
        msg['Subject'] = Header(subject, 'utf-8')
        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        filepath = filepath.strip()
        if os.path.isfile(filepath):
            contype = 'application/octet-stream'
            maintype, subtype = contype.split('/', 1)
            data = open(filepath, 'rb')
            file_msg = MIMEBase(maintype, subtype)
            file_msg.set_payload(data.read())
            data.close()
            email.encoders.encode_base64(file_msg)
            filename_list = filepath.split('/')
            filename = filename_list[len(filename_list) - 1]
            basename = os.path.basename(filename)
            file_msg.add_header('Content-Disposition', 'attachment', filename=basename)
            msg.attach(file_msg)
        is_send_success = False
        resend_times = 0
        for i in range(0, 3):
            smtp = ""
            try:
                smtp = smtplib.SMTP(smtpserver)
                smtp.login(username, password)
                # 用smtp发送邮件
                smtp.sendmail(sender, receiver, msg.as_string())
                is_send_success = True
                break
            except Exception as e:
                resend_times += 1
                user_logger.debug("发送第%s次失败！10秒后重试！" % resend_times)
                user_logger.error(traceback.format_exc())
                time.sleep(10)  # 休眠10秒，10秒后重发
                if len(receiver) == 0:
                    return False
            finally:
                if smtp != "":
                    smtp.quit()
        if is_send_success:
            return True
        else:
            return False
    except Exception as e:
        print(traceback.format_exc())
        return False



def whether_display_name(namestr):
    if re.match("^[\u4e00-\u9fa5]{2,4}\([a-z]{1,}[0-9]{0,}\)$", namestr):
        return True
    else:
        return False


if __name__ == "__main__":
    retstr = get_email_list("wangjiliang001@ke.com;wangjiliang@ke.com；王蕾(wanglei05);,wang@ke.com，")
    print(retstr)
    print(type(retstr))
