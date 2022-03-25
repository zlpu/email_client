# -*- coding:utf-8 -*-
#从Qt ui文件加载窗口界面
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
import smtplib
import string
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from PySide2.QtGui import  QIcon


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('email_client.ui')
        self.ui.send_Button.clicked.connect(self.sendmail)

    def sendmail(self):
        """
        计算处理部分,基本逻辑
        1.获取图形界面上输入的数据
        2.将数据做处理
        3.点击按钮的动作
        """
        # 定义发件地址信息
        Server_host = 'smtp.qq.com:465'
        From = '2925006354@qq.com'
        From_name=self.ui.fromname_TextEdit.toPlainText()
        PWD = 'Shggmjeddecg'

        # 定义邮件接收地址，过地址使用“,”隔开

        To_user=self.ui.address_TextEdit.toPlainText()
        To=To_user.split(",")#将多个收件人转换为列表To=['user1','user2'...]
        # print(To)
        # To_name="收件人名称"

        # 设置总的邮件体对象，对象类型为mixed
        msg = MIMEMultipart('mixed')

        # 定义邮件内容
        # 1.邮件主题内容
        msg_subject =self.ui.subject_TextEdit.toPlainText()

        # 2.正文部分
        # 2.1 纯文字部分内容
        msg_text = self.ui.body_TextEdit.toPlainText()
        # 2.2 图片内容
        image_path=self.ui.image_TextEdit.toPlainText()[8:]
        image_name=self.ui.image_TextEdit.toPlainText().split('/')[-1]
        msg_image = open(image_path, 'rb').read()

        # 2.3 附件内容
        file_path=self.ui.file_TextEdit.toPlainText()[8:]
        file_name = self.ui.file_TextEdit.toPlainText().split('/')[-1]
        msg_file = open(file_path, 'rb').read()

        # 3.构建消息体（符合smtp协议定义的格式）
        # 3.1 纯文字部分的消息体
        text_info = MIMEText(msg_text, 'plain', 'utf-8')  # 正文，三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        msg['From'] = Header(From_name, 'utf-8')    # 收件信息中显示的发件人名称，非真实的发件地址（非必须）
        # msg['To'] =  Header(To_name, 'utf-8')       # 发件信息中显示的接收者名称，非真实的收件地址（非必须）
        msg['Subject'] = Header(msg_subject, 'utf-8')  # 标题
        # 3.2 图片部分消息体
        image_info = MIMEImage(msg_image)
        image_info.add_header('Content-ID', '<image1>')
        image_info["Content-Disposition"] = 'attachment; filename='+image_name  # 如果不加这行代码的话，会在收件方方面显示乱码的bin文件，也可以对文件重命名
        # 3.3 附件文件消息体
        file_info = MIMEText(msg_file, 'base64', 'utf-8')
        file_info["Content-Type"] = 'application/octet-stream'
        file_info.add_header('Content-Disposition', 'attachment', filename=file_name)  # 可以重命名附件文件名

        # 写入邮件中()

        msg.attach(text_info)  # 纯文字部分
        msg.attach(image_info)  # 图片部分
        msg.attach(file_info)  # 附件部分

        # 发送邮件
        try:
            smtpObj = smtplib.SMTP_SSL(Server_host)  # 邮件服务器地址
            smtpObj.login(From, PWD)  # 发件人信息（账户，密码）
            smtpObj.sendmail(From, To, msg.as_string())  # 发送命令，as_string
            send_code='邮件发送成功'
        except smtplib.SMTPException as e:
            send_code='邮件发送失败\n' + str(e)

        QMessageBox.about(self.ui,"发送回执",send_code)
if __name__ == '__main__':

    app = QApplication([])
    app.setWindowIcon(QIcon('email_client_.png'))  # 运行时的窗口图标
    stats = Stats()
    stats.ui.show()
    app.exec_()