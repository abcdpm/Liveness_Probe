from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import logging
import requests
import smtplib
import configparser
from email.mime.text import MIMEText

nyaa_rss_url = 'https://nyaa.si/?page=rss&q=%5BNC-Raws%5D+RWBY%EF%BC%9A%E5%86%B0%E9%9B%AA%E5%B8%9D%E5%9B%BD&c=0_0&f=0'
dmhy_rss_url = 'https://share.dmhy.org/topics/rss/rss.xml?keyword=+%E5%96%B5%E8%90%8C%E5%A5%B6%E8%8C%B6%E5%B1%8B'

logging.basicConfig(
    filename="./logs/Liveness_Probe.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


def cf():
    cf = configparser.ConfigParser()
    filename = cf.read(r'./configs/Liveness_Probe.ini', encoding='utf-8')

    # sections() 得到所有的section，以列表形式返回
    sec = cf.sections()
    print(sec)

    # 得到section下的所有option
    opt = cf.options("email")
    print(opt)

    # items 得到section的所有键值对
    value = cf.items("email")
    print(value)
    print(dict(value))  # 转成字典类型1

    # get(section,option) 得到section中的option值，返回string/int类型的结果
    mysql_host = cf.get("email", "host")
    mysql_password = cf.getint("email", "port")
    print(mysql_host, mysql_password)


def email_send(text):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = '靓仔 <xx@qq.com>'
    msg['To'] = '靓仔 <xx@qq.com>'
    msg['Subject'] = '您的程序已执行完毕！'
    from_addr = 'xx@qq.com'
    from_password = 'xxxxxxxxxxxxxx'
    from_smtp_server = 'smtp.qq.com'
    to_addr = 'xx@qq.com'
    # QQ邮箱的SMTP服务需SSL加密，端口为465
    server = smtplib.SMTP_SSL(from_smtp_server)
    # 显示发送过程
    server.set_debuglevel(1)
    try:
        server.login(from_addr, from_password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    except Exception as e:
        logging.exception(f"main exception: {str(e)}")


def liveness_detect():
    try:
        data = requests.get(nyaa_rss_url)
        code = data.status_code
        if code != 200:
            logging.error("nyaa获取rss订阅异常")
        else:
            logging.info('{} nyaa_rss: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code))
    except Exception as e:
        logging.exception(f"main exception: {str(e)}")

    try:
        data = requests.get(dmhy_rss_url)
        code = data.status_code
        if code != 200:
            logging.error('dmhy获取rss订阅异常')
        else:
            logging.info('{} dmhy_rss: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code))
    except Exception as e:
        logging.exception(f"main exception: {str(e)}")


if __name__ == '__main__':
    liveness_detect()
    # my_scheduler = BlockingScheduler()
    # my_scheduler.add_job(liveness_detect, 'cron', minute='*/1')
    # my_scheduler.start()
