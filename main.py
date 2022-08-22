from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import requests

nyaa_rss_url = 'https://nyaa.si/?page=rss&q=%5BNC-Raws%5D+RWBY%EF%BC%9A%E5%86%B0%E9%9B%AA%E5%B8%9D%E5%9B%BD&c=0_0&f=0'
dmhy_rss_url = 'https://share.dmhy.org/topics/rss/rss.xml?keyword=+%E5%96%B5%E8%90%8C%E5%A5%B6%E8%8C%B6%E5%B1%8B'


def liveness_detection():
    try:
        data = requests.get(nyaa_rss_url)
        code = data.status_code
        if code != 200:
            print('nyaa获取rss订阅异常')
        else:
            print('{} nyaa_rss: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code))
    except Exception:
        print('nyaa获取rss订阅异常--连接超时')

    try:
        data = requests.get(dmhy_rss_url)
        code = data.status_code
        if code != 200:
            print('dmhy获取rss订阅异常')
        else:
            print('{} dmhy_rss: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code))
    except Exception:
        print('dmhy获取rss订阅异常--连接超时')


if __name__ == '__main__':
    my_scheduler = BlockingScheduler()
    my_scheduler.add_job(liveness_detection, 'cron', minute='*/1')
    my_scheduler.start()
