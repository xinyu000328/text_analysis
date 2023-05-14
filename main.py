import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
from selenium import webdriver
chrome_driver=r"D:\Program Files\Python\chromedriver.exe"
#driver=webdriver.Chrome(executable_path=chrome_driver)

# ['用户名','微博内容','点赞','评论数','转发数','评论用户名','评论内容','评论时间']

# 判断是否有展开全文
def is_exist_z(web):
    try:
        txt = web.find_element_by_xpath('./div/div/div/article/div/div[1]/a[4]').text
        if txt == '全文':
            return True
        else:
            return False
    except:
        return False

# 获取评论
def get_comment(div,web):
    # 点击评论展开
    button = div.find_element_by_xpath('./div/div/div/article/div/div[1]')
    web.execute_script("arguments[0].click()", button)
    # button = div.find_element_by_xpath('./div/div/div/article/div/div[1]')
    # web.execute_script("arguments[0].click()",button)
    time.sleep(3)
    # div.switch_to.window(div.window_handles[0])
    # time.sleep(1)
    # 获取评论内容
    comment_info = []
    comment_div_list = web.find_elements_by_xpath('//*[@id="app"]/div[1]/div/div[4]/div[2]/div')
    print('length:',len(comment_div_list))
    for div_t in comment_div_list[:-1]:     # 通过切片去除最后一个元素
        comment_info_test = []
        comment_user = div_t.find_element_by_xpath('./div/div/div/div/div[2]/div[1]/div/div/h4').text
        comment_detail = div_t.find_element_by_xpath('./div/div/div/div/div[2]/div[1]/div/div/h3').text
        comment_time = div_t.find_element_by_xpath('./div/div/div/div/div[2]/div[2]/div').text
        # print('user:',comment_user)
        comment_info_test.append(comment_user)
        comment_info_test.append(comment_detail)
        comment_info_test.append(comment_time)
        temp_list = comment_info_test[:]
        # 保存数据
        comment_info.append(temp_list)
        '''
        a.extend(b)     将b列表中的元素逐个追加到a列表  
        a.append(b)     将对象添加到a列表
        '''

    web.back()

    return comment_info

# 登录
def login():
    url = 'https://m.weibo.cn/'
    opt = Options()
    # 删掉Chrome浏览器正在受到自动测试软件的控制
    opt.add_experimental_option('excludeSwitches',['enable-automation'])
    # 创建浏览器对象
    web = Chrome(options=opt)
    web.get(url)
    input("是否完成登录？")
    return web

# 点击热门
def click_hot(web):
    # 点击热门
    web.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div/ul/li[3]/span').click()
    time.sleep(5)

    # 控制滑动
    count = 0
    while count < 1:
        web.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(3)
        count += 1

    return web

# 爬取数据
def page_spider():
    # 写入文件
    f = open('./三连加关注.csv',mode='w',encoding='ANSI',newline='')
    writer = csv.writer(f)
    writer.writerow(['用户名','微博内容','点赞数','评论数','转发数','评论用户','评论内容','评论时间'])

    # 登录
    web = login()
    # 跳转到搜索页面
    web.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/a/aside/label/div').click()
    time.sleep(2)
    # data = input('请输入话题：')
    data = '#春暖花开的3月来了#'
    web.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/div/div[2]/form/input').send_keys(data,
                                                                                                         Keys.ENTER)
    time.sleep(3)

    '''
    '用户名','微博内容','点赞数','评论数','转发数','评论用户','评论内容','评论时间'  
    '''
    # 点击热门
    web = click_hot(web)
    # 所有微博所在的div
    div_list = web.find_elements_by_xpath('//*[@id="app"]/div[1]/div[1]/div')
    div_count = 3
    while div_count < len(div_list):
        time.sleep(10)
        # 点击热门
        web = click_hot(web)
        # 所有微博所在的div
        div_list = web.find_elements_by_xpath('//*[@id="app"]/div[1]/div[1]/div')
        for div in div_list[div_count:]:
            comment_info_detail = []
            user_name = div.find_element_by_xpath('./div/div/div/header/div/div/a/h3').text
            if is_exist_z(div) == True:
                # 获得全文链接
                detail_page_content_url = div.find_element_by_xpath('./div/div/div/article/div/div[1]/a[4]').get_attribute(
                    'href')
                print("url ： ", detail_page_content_url)
                # 使用js语句打开链接
                js = "window.open('" + detail_page_content_url + "');"
                web.execute_script(js)
                time.sleep(10)
                # 切换窗口
                web.switch_to.window(web.window_handles[1])
                time.sleep(10)
                # 获取全文
                page_detail = web.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div/article/div/div/div[1]').text
                # 关闭子窗口
                web.close()
                # 切换回原来的窗口
                web.switch_to.window(web.window_handles[0])
            else:
                page_detail = div.find_element_by_xpath('./div/div/div/article/div/div[1]').text
            praise = div.find_element_by_xpath('./div/div/div/footer/div[3]/h4').text
            comment = div.find_element_by_xpath('./div/div/div/footer/div[2]/h4').text

            tran = div.find_element_by_xpath('./div/div/div/footer/div[1]/h4').text
            print('user name:', user_name)
            print('page_detail:', page_detail)
            print('praise:', praise)
            print('comment:', comment)
            print('tran:', tran)
            time.sleep(1)
            comment_info_detail = get_comment(div,web)
            writer_list = []
            writer_list.append(user_name)
            writer_list.append(page_detail)
            writer_list.append(praise)
            writer_list.append(comment)
            writer_list.append(tran)
            for detail in comment_info_detail:
                print(detail)
                writer_list.append(detail[0])
                writer_list.append(detail[1])
                writer_list.append(detail[2])
                writer.writerow(writer_list)
                print('*'*100,writer_list)
                del writer_list[5:8]
            # f.close()
            # comment_info_detail.shape ： [['user4', 'detail4', 'time4'],['user4', 'detail4', 'time4'],['user4', 'detail4', 'time4']……]
            div_count += 1
            break
    f.close()



if __name__ == '__main__':
    page_spider()

# button = div.find_element_by_xpath('./div/div/div/article/div/div[1]')