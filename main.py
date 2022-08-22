from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import logging
import requests
import smtplib
import configparser
from email.mime.text import MIMEText

nyaa_rss_url = 'https://nyaa.si/?page=rss&q=%5BNC-Raws%5D+RWBY%EF%BC%9A%E5%86%B0%E9%9B%AA%E5%B8%9D%E5%9B%BD&c=0_0&f=0'
dmhy_rss_url = 'https://share.dmhy.org/topics/rss/rss.xml?keyword=+%E5%96%B5%E8%90%8C%E5%A5%B6%E8%8C%B6%E5%B1%8B'
nyaa_flag = True
dmhy_flag = True

logging.basicConfig(
    filename="./logs/Liveness_Probe.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


def email_send(text):
    # read config from Liveness_Probe.ini
    cf = configparser.ConfigParser()
    cf.read(r'./configs/Liveness_Probe.ini', encoding='utf-8')

    # set the email configs
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = cf.get("email", "from")
    msg['To'] = cf.get("email", "to")
    msg['Subject'] = cf.get("email", "subject")
    from_addr = cf.get("email", "from_addr")
    from_password = cf.get("email", "from_password")
    from_smtp_server = cf.get("email", "from_smtp_server")
    to_addr = cf.get("email", "to_addr")

    try:
        server = smtplib.SMTP_SSL(from_smtp_server)
        server.set_debuglevel(1)
        server.login(from_addr, from_password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        logging.info("邮件发送成功!")
    except Exception as e:
        logging.exception(f"main exception: {str(e)}")


def liveness_detect():
    global nyaa_flag, dmhy_flag

    try:
        data = requests.get(nyaa_rss_url)
        code = data.status_code
        logging.info('{} nyaa_rss: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code))
        nyaa_flag = True
    except Exception as e:
        if nyaa_flag:
            nyaa_flag = False
            email_send("nyaa获取rss订阅异常")
            logging.exception(f"main exception: {str(e)}")

    try:
        data = requests.get(dmhy_rss_url)
        code = data.status_code
        logging.info('{} dmhy_rss: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code))
        dmhy_flag = True
    except Exception as e:
        if dmhy_flag:
            dmhy_flag = False
            email_send("dmhy获取rss订阅异常")
            logging.exception(f"main exception: {str(e)}")


if __name__ == '__main__':
    # email_send("test")
    # liveness_detect()
    my_scheduler = BlockingScheduler()
    my_scheduler.add_job(liveness_detect, 'cron', minute='*/1')
    my_scheduler.start()
