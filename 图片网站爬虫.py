import requests
import parsel
import os

for page in range(1, 6):
    print('==============================正在爬取第{}页数据========================='.format(page))
    # 1.确定网页性质和地址
    base_url = 'http://www.win4000.com/meinvtag26_{}.html'.format(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4043.400'}

    # 2.发送请求
    response = requests.get(url=base_url, headers=headers)
    response.encoding = 'utf-8'
    data = response.text
    # print(data)

    # 3.数据解析--解析出我们想要的数据
    html_data = parsel.Selector(data)
    data_list = html_data.xpath(
        '//div[@class="Left_bar"]//ul/li/a/@href|//div[@class="Left_bar"]//ul/li/a/img/@title').extract()
    # print(data_list)

    data_list = [data_list[i:i + 2] for i in range(0, len(data_list), 2)]
    #     遍历列表元素
    for alist in data_list:
        html_url = alist[0]
        file_name = alist[1]
        #       print(html_url,file_name)

        if not os.path.exists(r'D:\\电脑桌面\\编程\\img\\' + file_name):
            os.mkdir(r'D:\\电脑桌面\\编程\\img\\' + file_name)
        print('正在下载：', file_name)

        #     发送详情页请求，解析总页数
        response_2 = requests.get(html_url, headers=headers).text
        html_2 = parsel.Selector(response_2)
        page_num = html_2.xpath('//div[@class="ptitle"]//em/text()').extract_first()
        print(page_num)

        for url in range(1, int(page_num) + 1):
            url_list = html_url.split('.')
            all_url = url_list[0] + '.' + url_list[1] + '.' + url_list[2] + '_' + str(url) + '.' + url_list[3]

            response_3 = requests.get(all_url, headers=headers).text
            html_3 = parsel.Selector(response_3)
            img_url = html_3.xpath('//div[@class="pic-meinv"]//img/@data-original').extract_first()
            #         print(img_url)

            img_data = requests.get(img_url, headers=headers).content
            img_name = str(url) + '.jpg'

            with open(r'D:\\电脑桌面\\编程\\img\\{}\\'.format(file_name) + img_name, 'wb') as f:
                print('下载完成：', img_name)
                f.write(img_data)
print('下载完成！！！')