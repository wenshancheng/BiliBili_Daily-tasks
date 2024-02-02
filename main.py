import time, requests_html, random
from determine import handle_cookie,determine,multiply,exchange_silver,get_pop_video

Session = requests_html.HTMLSession()
Sleeptime = 1   #控制代码运行延迟

class request:
    def __init__(self):
        self.headers = {"User-Agent" : requests_html.UserAgent().random, "Referer": "https://www.bilibili.com/",}

    def get(self, list) -> dict: # list["url","cookie"] 处理get请求
        res = Session.get(url=list[0], headers=self.headers,cookies=list[1]).json()
        return res
        
    def post(self, list) -> dict: # list["url","cookie","data"] 处理post请求
        res = Session.post(url=list[0], headers=self.headers,cookies=list[1],data=list[2]).json()
        return res

class put:
    def __init__(self):     #API
        self.url = {
        "Bili_UserData" : "http://api.bilibili.com/x/space/myinfo",
        "Bili_live": "https://api.live.bilibili.com/sign/doSign",
        "Silver_Melon" : "https://api.live.bilibili.com/xlive/web-ucenter/user/get_user_info",
        "Silver_Exchange" : "https://api.live.bilibili.com/pay/v1/Exchange/silver2coin",
        "Bili_Sign": "https://api.bilibili.com/x/web-interface/nav/stat",
        "Hot_Video" : "https://api.bilibili.com/x/web-interface/popular?ps=50&pn=1",
        "Shave_Video" : "https://api.bilibili.com/x/web-interface/share/add",
        "Look_Video" : "https://api.bilibili.com/x/click-interface/web/heartbeat",
        "Coin" : "http://account.bilibili.com/site/getCoin",
        "Put_Coin" : "https://api.bilibili.com/x/web-interface/coin/add",
        "Get_Exp" :"https://api.bilibili.com/x/web-interface/coin/today/exp"
        }

    def get_userdata(self, cookie:dict) -> bool:  #获取用户信息
        print("\n#正在获取用户基本信息#"); time.sleep(Sleeptime)
        res = request().get([self.url['Bili_UserData'],cookie])
        if res['code'] == -101 : return False
        else:
            Data = []
            res = res['data']
            Data_Name = ['name', 'mid', 'coins', 'level'] 
            for i in Data_Name: Data.append(str(res[i]))
            res = res['level_exp']
            Data_Name = ['current_exp','next_exp']
            for i in Data_Name: Data.append(res[i])     #["名字","ID","硬币","等级","当前经验","下级经验"]
        print("😎 :"+Data[0]+" 😮 :"+Data[1]+" 当前有"+Data[2]+"个硬币🤑")
        print("当前🌵:"+Data[3]+" 当前📖:"+str(Data[4])+" 下一级📖:"+str(Data[5])+" 还需:"+str(Data[5]-Data[4])+"📖")

    def sgin_in_live(self, cookie:dict):   #B站直播签到+兑换银瓜子
        print("\n#正在进行B站直播签到#"); time.sleep(Sleeptime)
        res = request().get([self.url['Bili_live'],cookie])
        if res['code'] == 1011040:  print("B站直播你已经签到过啦😁")
        else:   print("本月签到"+str(res['data']['hadSignDays'])+"次,本次签到奖励👉 "+res['data']['text']+" 👈")
        res = request().get([self.url['Silver_Melon'],cookie]); res = res['data']
        if exchange_silver(res['silver']) == True:
            post = {"csrf_token" : cookie['bili_jct'],"csrf" : cookie['bili_jct']}
            res = request().post([self.url['Silver_Exchange'],cookie,post])
            if res['code'] == 0:  print("兑换成功😆")
            else: print("兑换异常😨(银瓜子兑换)")
            
    def sgin_video(self, cookie:dict):   #B站签到
        print("\n#正在进行B站视频签到#"); time.sleep(Sleeptime)
        res = request().get([self.url['Bili_Sign'],cookie])
        if res['code'] == -101: print("签到出现异常,请及时检查😨(签到)")
        else: print(time.strftime("%m月%d日签到完成,本次签到获得5EXP"))

    def get_pop_video(self,cookie:dict,num:int) -> list: #获取随机视频或指定UP视频
        print("\n#正在获取一堆视频#"); time.sleep(Sleeptime)
        get_video = get_pop_video(num); Aid_Data = []
        if get_video == True:
            print("正在获取随机视频")
            res = request().get([self.url['Hot_Video'], cookie])
            res = res['data']['list']
            for i in res: Aid_Data.append(i['aid'])
            print("获取结束")
            return Aid_Data
        else:
            for i in get_video:
                if type(i) != int: print("你指定的UID有问题😦")
                else:
                    print("正在获取你指定的UID视频")
                    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?host_mid="+str(i)
                    res = request().get([url,cookie])
                    for i in res['data']['items']: 
                        try: Aid_Data.append(i['modules']['module_dynamic']['major']['archive']['aid'])
                        except: pass
                    print("获取结束")
                    return Aid_Data
        
    def shave_video(self,cookie:dict,Aid_Data:list):  #随机分享一个视频
        print("\n#正在随机分享一个视频#"); time.sleep(Sleeptime)
        post = {"aid" : Aid_Data[random.randint(0, 40)] , "csrf" : cookie["bili_jct"]}
        res = request().post([self.url['Shave_Video'],cookie,post])
        if res['code'] == 0: print(time.strftime("%m月%d日视频分享成功,本次分享获得5EXP"))
        elif res['code'] == 71000: print("重复分享了🙄")
        else : print("分享异常😨")
    
    def look_video(self,cookie:dict,Aid_Data:list):    #随机观看一个视频
        print("\n#正在随机观看一个视频#"); time.sleep(Sleeptime)
        post = {"aid":Aid_Data[random.randint(0, 39)],"csrf":cookie["bili_jct"], "played_time" : random.randint(33, 66)}; 
        res = request().post([self.url['Look_Video'],cookie,post])
        if res['code'] == 0: print(time.strftime("%m月%d日观看视频完成,本次观看获得5EXP"))
        else : print("随机观看视频异常😨")
    
    def put_coin(self,list):    #向视频投币
        aid = list[0]; num = 0; err = 0
        while True:
            time.sleep(Sleeptime)
            if num >= list[2]: print("随机投币完成,共获得"+str(num*10)+"EXP😃"); break
            elif err > 10: print("多次投币异常,结束随机投币,请检查投币是否正常😨"); break
            else:
                Coin = multiply()
                post = {'aid': aid[random.randint(0,49)],'multiply': Coin,'select_like': 0,'cross_domain': 'true','ramval': 0,'csrf': list[1]['bili_jct']}
                if Coin == 2:
                    res = request().post([self.url['Put_Coin'],list[0],post]); num+=2
                else:
                    res = request().post([self.url['Put_Coin'],list[0],post]); num+=1               
                if res['code'] == 0: print('正在投出'+str(num)+'个硬币')
                elif res['code'] == 34005: print("超过投币上限啦")
                else: err+=1; print("投币请求异常")

    def get_coining_exp(self,cookie:dict,Aid_Data:list): #判断用户硬币和投币经验
        print('\n#正在进行视频投币#'); time.sleep(Sleeptime)
        exp = request().get([self.url['Get_Exp'],cookie]); exp = 50 - exp['data']
        coin = request().get([self.url['Coin'],cookie]); coin = coin['data']['money']
        num = determine(exp,coin)
        if num == 0:
            return
        else:
            put().put_coin([Aid_Data,cookie,num])
        
        
    def run():  #取得用户cookie并运行
        num = 0
        for cookie in handle_cookie():
            num+=1
            print("\n"+"*"*10+"正在执行第" + str(num) + "个cookie"+"*"*10); 
            boolean = put().get_userdata(cookie)
            if boolean == False: 
                print("Bili_cookie出现异常,请及时检查😨")
                continue
            else:   
                put().sgin_in_live(cookie)
                put().sgin_video(cookie)
                Aid_Data = put().get_pop_video(cookie,num)
                put().look_video(cookie,Aid_Data)
                put().shave_video(cookie,Aid_Data)
                put().get_coining_exp(cookie,Aid_Data)
            print("\n"+"*"*10+"第" + str(num) + "个cookie执行结束"+"*"*10); 

put.run()

