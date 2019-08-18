from email import charset
charset.add_charset('utf-8', charset.SHORTEST, charset.BASE64, 'utf-8')

import datetime,os
import smtplib
from email.mime.multipart import MIMEMultipart  #import email.MIMEMultipart
from email.mime.text import MIMEText            #import email.MIMEText
from email.mime.base import MIMEBase            #import email.MIMEBase
from email.header import Header
import email.encoders
from core.tools.VerifyTool import VerifyTool
import platform,logging
from  core.config.InitConfig import EmailConfig
import traceback,time
from core.tools.TypeTool import TypeTool

class UsualTool(object):
    """常用函数"""

    @staticmethod
    def get_current_time():
        #return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_current_time_numstr():
        # return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    @staticmethod
    def send_mail(email_list,subject,emailText,filepath = "",subType = "text"):
        try:
            #发送email
            receiver = []
            receivertmp = email_list.split(';')
            for mail in receivertmp:
                if VerifyTool.IsEmail(mail):
                    receiver.append(mail)

            sender = EmailConfig.sender
            smtpserver = EmailConfig.smtpserver
            username = EmailConfig.username
            password = EmailConfig.password

            # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
            msg=MIMEMultipart() #
            if subType == "text":
                text_msg = MIMEText(emailText, 'plain', 'utf-8') #文本格式
            elif subType == "html":
                text_msg = MIMEText(emailText, _subtype='html', _charset='utf-8')  # html格式
            else:
                text_msg = MIMEText(emailText, 'plain', 'utf-8')  # 文本格式

            msg.attach(text_msg)
            msg['From'] = sender
            msg['To'] =  ";".join(receiver)
            msg['Subject'] = Header(subject, 'utf-8')
            # 构造MIMEBase对象做为文件附件内容并附加到根容器
            ## 读入文件内容并格式化
            filepath = filepath.strip()
            if os.path.isfile(filepath):
                contype = 'application/octet-stream'
                maintype, subtype = contype.split('/', 1)
                data = open(filepath, 'rb')
                file_msg = MIMEBase(maintype, subtype)
                file_msg.set_payload(data.read( ))
                data.close( )
                email.encoders.encode_base64(file_msg)
                ## 设置附件头
                filename_list = filepath.split('/')
                filename = filename_list[len(filename_list)-1]
                basename = os.path.basename(filename)
                file_msg.add_header('Content-Disposition', 'attachment', filename = basename)
                msg.attach(file_msg)
            isSendSuccess = False
            resendTimes = 0
            for i in range(0,2):
                try:
                    smtp = ""
                    smtp = smtplib.SMTP(smtpserver)
                    smtp.login(username, password)
                    # 用smtp发送邮件
                    smtp.sendmail(sender, receiver, msg.as_string())
                    isSendSuccess = True
                    break
                except Exception as e:
                    resendTimes += 1
                    time.sleep(10) #休眠10秒，10秒后重发
                    logging.info("subject[%s]发送失败，重发%d！%s" % (subject,resendTimes,traceback.format_exc()))
                    if len(email_list) == 0:
                        return False
                finally:
                    if TypeTool.is_str(smtp) == False:
                        smtp.quit()
            if isSendSuccess:
                logging.info("DONE:send subject[%s] email to %s,receiver is [%s],RetryTimes[%d]" % (subject,email_list,receiver,resendTimes))
                return True
            else:
                logging.info("NOTSEND:send subject[%s] email to %s,receiver is [%s],RetryTimes[%d]" % (subject,email_list,receiver,resendTimes))
                return False
        except Exception as e:
            logging.error(traceback.format_exc())
            return False

    @staticmethod
    def encrypt(infos):
        encryptInfos = ''
        for i in range (0,len(infos)):
            if i == len(infos): break
            encryptInfos = encryptInfos + str(hex(ord(infos[i])))[-2:]
        #print encryptInfos
        return encryptInfos

    @staticmethod
    def decrypt(encryptedInfos):
        decryptInfos = ""
        for i in range(0,len(encryptedInfos),2):
            hextoint = int("%s%s" % (encryptedInfos[i],encryptedInfos[i+1]),16)
            decryptInfos = decryptInfos + chr(hextoint)
        #print decryptInfos
        return decryptInfos

    @staticmethod
    def isWindowsSystem():
        return 'Windows' in platform.system()

    @staticmethod
    def isLinuxSystem():
        return 'Linux' in platform.system()

    @staticmethod
    def isMacOS():
        return 'Darwin' in platform.system()


