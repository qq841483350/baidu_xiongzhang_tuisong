#coding:utf8
#python编写的百度熊掌号资源提交工具GUI,url一行一个
import requests,time,wx,re
def xiongzhang(event):
    content_url=content2.GetValue()  #获取content2里的内容  获取到所有的URL
    if content_url:
        content_url=content_url+'\nhttp'  #为了正则匹配到最后一个URL，在最后加上一个换行和http
        urls=re.findall('(.*?)\s+',content_url)  #正则获取所有URL为一个列表
        tuisong_urls='\n'.join(urls)  #把这个列表中所有的URL以换行做分隔。
        # print tuisong_urls
        post_url=content1.GetValue()  #获取content1里的内容即：接口调用地址
        post_url=str(post_url).strip()
        # filecontents={'file':open('urls.txt','r')}  #如果把所有urls放到本地的urls.txt里每行一个，则用这种方法来推送
        # r=requests.post(post_url,files=filecontents)
        if requests.post(post_url,data=tuisong_urls):  #开始推送
            r=requests.post(post_url,data=tuisong_urls)
            result=r.text.decode('utf8')
            print result
            # print result
            if 'success_realtime' in result:
                x=re.findall('"success_realtime":(\d+),"remain_realtime":(\d+)',result)
                success_realtime=str(x[0][0]) #成功推送的url条数
                remain_realtime=str(x[0][1])  #今天剩余可推送的url条数
                result_content='\n推送完成：\n成功推送的url条数:'+success_realtime+'\n今天剩余可推送的url条数:'+remain_realtime
                print result_content

                # content3.SetValue(result_content)   #结果填充到content3中，覆盖式的
                wx.MessageBox(result_content)  #弹出消息
                content2.Clear() #清空内容
                # content3.AppendText(result_content)  #结果填充到content3中，非覆盖，在最后一行添加
            elif 'not_valid' in result:
                result='推送失败,url不符合要求，请重新填写'
                # print result
                wx.MessageBox(result)
                content2.Clear() #清空内容
            else:
                result='推送失败'
                wx.MessageBox(result)
                content2.Clear() #清空内容

        else:
            result_erro='\n推送失败,请检查接口调用地址是否正确'
            # content3.SetValue(result_erro)
            wx.MessageBox(result_erro)   #弹出消息
            content2.Clear() #清空内容
    else:
        result_erro_nourl='推送失败,URL为空,请填入需要提交的URL'
        wx.MessageBox(result_erro_nourl)   #弹出消息
        content2.Clear() #清空内容


if __name__=="__main__":
    app=wx.App()
    win=wx.Frame(None,title="【百度熊掌号资源批量提交工具】使用方法：填入接口地址与URL然后点击提交运行 《开发者:李亚涛,微信:841483350》".decode('utf8'),size=(850,700))
    icon=wx.Icon('favicon.ico',wx.BITMAP_TYPE_ICO)
    win.SetIcon(icon)
    win.Show()
    wx.StaticText(win,label="*接口调用地址:",pos=(100,12),size=(80,30))
    # content1=wx.TextCtrl(win,pos=(185,5),size=(500,30),style = wx.TE_MULTILINE | wx.TE_RICH)
    content1=wx.TextCtrl(win,pos=(185,5),size=(500,30))

    wx.StaticText(win,label="*请在下方填入需要提交的URL地址，一行一个,然后点击提交",pos=(100,40),size=(500,30))
    content2=wx.TextCtrl(win,pos=(100,70),size=(640,550),style=wx.TE_MULTILINE|wx.TE_RICH)
    loadButton=wx.Button(win,label='提交'.decode('utf8'),pos=(690,5),size=(50,30))
    loadButton.Bind(wx.EVT_BUTTON,xiongzhang)  #这个按钮绑定xiongzhang这个函数

    app.MainLoop()
xiongzhang()
