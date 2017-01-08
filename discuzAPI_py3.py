# -*- coding: utf-8 -*-

import requests
import re
import time
#from mysqlAPI import mysqlAPI

class DiscuzAPI:
    def __init__(self, forumUrl, userName, password, proxy = None):
        ''' 初始化论坛url、用户名、密码和代理服务器 '''
        self.forumUrl = forumUrl
        self.userName = userName
        self.password = password
        self.formhash = ''
        self.isLogon = False
        self.isSign = False
        self.xq = ''
        self.rq = requests.session()   

    def login(self):
        ''' 登录论坛 '''
        url = self.forumUrl + "/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&inajax=1";
        postData = {'username': self.userName, 'password': self.password, 'answer': '', 'cookietime': '2592000', 'handlekey': 'ls', 'questionid': '0', 'quickforward': 'yes',  'fastloginfield': 'username'}
#        rq = requests.session()        
        html = self.rq.post(url,postData)
        print(html.text)
        if self.userName in html.text:
            self.isLogon = True
            print ('logon success!')
            self.initFormhashXq()
            return 1
        else:
            print ('logon faild!')
            return 0
            
    def initFormhashXq(self):
        ''' 获取formhash和心情 '''
        html = self.rq.get(self.forumUrl + '/plugin.php?id=dsu_paulsign:sign')
        
#        content = urllib2.urlopen(self.forumUrl + '/plugin.php?id=dsu_paulsign:sign').read().decode('utf-8')
        rows = re.findall(r'<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />', html.text)
#        print(rows)
        if len(rows)!=0:
            self.formhash = rows[0]
            print ('formhash is: ' + self.formhash)
        else:
            print ('none formhash!')
        rows = re.findall(r'<input id=.* type=\"radio\" name=\"qdxq\" value=\"(.*?)\" style=\"display:none\">', html.text)
        if len(rows)!=0:
            self.xq = rows[0]
            print ('xq is: ' + self.xq)
        elif u'已經簽到' in html.text:
            self.isSign = True
            print ('signed before!')
        else:
            print ('none xq!')

    def reply(self, tid, subject = u'',msg = u'支持~~~顶一下下~~嘻嘻'):
        ''' 回帖 '''
        url = self.forumUrl + '/forum.php?mod=post&action=reply&fid=41&tid='+str(tid)+'&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'
        postData = {'formhash': self.formhash, 'message': msg, 'subject': subject, 'posttime':int(time.time()) }
        html = self.rq.post(url,postData)        

#        print (html.text)
        if u'回復發佈成功' in html.text:
            print ('reply success!',tid,time.ctime())
        else:
            print(html.text)
#            print ('reply faild!',tid,time.ctime())

    def sign(self,msg = u'哈哈，我来签到了！'):
        ''' 签到 '''
        if self.isSign:
            return
        if self.isLogon and self.xq:
            url = self.forumUrl + '/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'
            postData = {'fastreply': '1', 'formhash': self.formhash, 'qdmode': '1', 'qdxq': self.xq, 'todaysay':msg }
            html = self.rq.post(url,postData)        
#            print (html.text)
            if u'成功' in html.text:
                self.isSign = True
                print ('sign success!')
                return
        print ('sign faild!')
 
    def speak(self,msg = u'hah,哈哈，测试一下！'):
        ''' 发表心情 '''
        url = self.forumUrl + '/home.php?mod=spacecp&ac=doing&handlekey=doing&inajax=1'
        postData = {'addsubmit': '1', 'formhash': self.formhash, 'referer': 'home.php', 'spacenote': 'true', 'message':msg }
        html = self.rq.post(url,postData)        
#        print (html.text)
        if u'操作成功' in html.text:
            print ('speak success!')
        else:
            print(html.text)
#            print ('speak faild!')
   
if __name__ == '__main__':
    url = 'http://hkbbcc.net/'
    discuz =  DiscuzAPI(url,user,password)   
    discuz.login()
#    discuz.sign()
    discuz.speak('今日到此一游！' + time.strftime('%y-%m-%d'))
#    discuz.reply(4201573)
    