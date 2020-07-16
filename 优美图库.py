# 优美图库2--->翻页效果
import requests
import parsel

for page in range (1,4):
    print('==============================正在爬取第{}页数据========================='.format(page))
    base_url='https://www.umei.cc/meinvtupian/meinvxiezhen/{}.htm'.format(str(page))
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3756.400 QQBrowser/10.5.4043.400'}

    response= requests.get(base_url,headers=headers)
    response.encoding = response.apparent_encoding
    html= response.text
    # print(html)
    parse = parsel.Selector(html)
    # print(parse)
    href_list = parse.xpath('//div[@class= "TypeList"]/ul/li/a/@href').extract()
    # print(href_list)
    for href in href_list:
    #     print(href)
        href_data=requests.get(href,headers=headers).text
        img = parsel.Selector(href_data)
        img_src = img.xpath('//div[@class="ImageBody"]/p/a/img/@src').extract_first()
    #     print(img_src)
        img_data = requests.get(img_src,headers=headers).content
        file_name = img_src.split('/')[-1]
    #     print(file_name)

        with open (r'D:\\电脑桌面\\编程\\img2\\'+file_name,'wb') as f:
            print('下载完成：', file_name)
            f.write(img_data)
print('\n'+'爬虫运行完毕！！！')