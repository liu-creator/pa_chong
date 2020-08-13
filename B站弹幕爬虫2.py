import requests
import jieba
import csv
import re
import threading
import time
from fake_useragent import UserAgent
import wordcloud


def func():
    # 在主函数里调用线程,这里省略
    # for page in range(7, 12):

    # print('==============================正在爬取第{}页数据========================='.format(page))
    # 1.确定网页性质和地址
    page_tag = page
    base_url = "https://api.bilibili.com/x/v2/dm/history?type=1&oid=221567942&date=2020-08-{}".format(page)
    ua = UserAgent()  # 用随机请求头替换之前的一个请求头
    headers = {'User-Agent': ua.random,
               "cookie": "_uuid=DAEAB3A5-A5EF-EDE2-2AA9-189B49B854C557143infoc; buvid3=4C59E5E1-1E34-4752-A989-95F6C652F0F240936infoc; sid=kx0no17b; DedeUserID=264442403; DedeUserID__ckMd5=a140d3f4b2d19818; SESSDATA=557104f3%2C1610466581%2Cd70a9*71; bili_jct=cf44b86b98e284868d8f68ee4298de40; CURRENT_FNVAL=16; rpdid=|(u~RJmY)uJR0J'ulml|||R|l; LIVE_BUVID=AUTO7315950824188063; CURRENT_QUALITY=80; bp_video_offset_264442403=422618352361401397; PVID=1; bp_t_offset_264442403=422640102081187060; bfe_id=1e33d9ad1cb29251013800c68af42315"
               }

    # 2.发送请求
    response = requests.get(url=base_url, headers=headers)
    response.encoding = 'utf-8'

    data = response.content.decode('utf-8')
    # print(data)

    # 3.数据解析--解析出我们想要的弹幕文字
    res = re.compile('<d.*?>(.*?)</d>')
    danmu = re.findall(res, data)
    # print(page_tag,danmu,'\n')
    print(page_tag, len(danmu), danmu, '\n')

    # 4.保存弹幕
    for i in danmu:
        with open(r'D:\电脑桌面\编程\法2_B站弹幕.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            danmu = []
            danmu.append(i)
            writer.writerow(danmu)


def func_word():
    # 词云图
    f = open(r'D:\电脑桌面\编程\法2_B站弹幕.csv', encoding='utf-8')
    txt = f.read()

    txt_list = jieba.lcut(txt)
    # print(txt_list)
    string = " ".join(txt_list)
    # print(string)
    w = wordcloud.WordCloud(
        width=1000,
        height=700,
        background_color='white',
        font_path="msyh.ttc",
        scale=15,
        stopwords={" ","哔哩","这次","一定"},
        contour_width=5,
        contour_color='red'
    )
    w.generate(string)
    w.to_file(r'D:\电脑桌面\编程\法2_B站弹幕词云图.png')
    time.sleep(1)


if __name__ == '__main__':
    for page in range(1, 13):
        if page < 10:
            page = str(page)
            page = page.zfill(2)
            sub_process = threading.Thread(target=func)

            sub_process.start()
            time.sleep(0.5)
        else:
            sub_process = threading.Thread(target=func)

            sub_process.start()
            time.sleep(0.5)

    func_word()
    print('完成！！！')
