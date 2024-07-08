import time,requests_html,random
from determine import user_config

Session = requests_html.HTMLSession()
Sleeptime = 1  # 控制代码运行延迟 1s


class Request:
    def __init__(self):
        self.headers = {"User-Agent": requests_html.UserAgent().random,
                        "Referer": "https://space.bilibili.com", }

    def get(self, list) -> dict: # list["url","cookie"] 处理get请求
        res = Session.get(url = list[0], headers=self.headers, cookies=list[1])
        return res

    def post(self, list) -> dict:  # list["url","cookie","data"] 处理post请求
        res = Session.post(url=list[0], headers=self.headers, cookies=list[1], data=list[2])
        return res


class RunTask():
    def __init__(self):
        self.url = {
            "Bili_UserData": "http://api.bilibili.com/x/space/myinfo",
            "Bili_live": "https://api.live.bilibili.com/sign/doSign",
            "Silver_Melon": "https://api.live.bilibili.com/xlive/web-ucenter/user/get_user_info",
            "Silver_Exchange": "https://api.live.bilibili.com/pay/v1/Exchange/silver2coin",
            "Bili_Sign": "https://api.bilibili.com/x/web-interface/nav/stat",
            "Hot_Video": "https://api.bilibili.com/x/web-interface/popular?ps=50&pn=1",
            "Shave_Video": "https://api.bilibili.com/x/web-interface/share/add",
            "Look_Video": "https://api.bilibili.com/x/click-interface/web/heartbeat",
            "Coin": "http://account.bilibili.com/site/getCoin",
            "Put_Coin": "https://api.bilibili.com/x/web-interface/coin/add",
            "Get_Exp": "https://api.bilibili.com/x/web-interface/coin/today/exp"
        }

    def get_user_data(self, cookie:dict) -> bool:      # 获取用户信息
        print("\n#正在获取用户基本信息#");time.sleep(Sleeptime)
        try:
            response = Request().get([self.url['Bili_UserData'], cookie])
            if response.status_code != 200:
                print("请求失败😨请检查网址是否能用"); return False
            res = response.json()
            if res['code'] == -101:
                print("cookie错误😨请检查cookie是否正确"); return False
            
            res = res['data']; UD = []
            for key in ['name', 'mid', 'coins', 'level']:
                if key not in res:
                    print(f"数据缺失:{key}"); return False
                else:
                    UD.append(str(res[key]))

            res = res['level_exp']
            for key in ['current_exp', 'next_exp']:
                if key not in res:
                    print(f"数据缺失:{key}"); return False
                else:
                    UD.append(res[key])

            print("😀: "+ UD[0] + " mid: "+UD[1] + " 当前还有硬币: "+ UD[2]+ "个🤑")
            print("当前🌵: "+UD[3]+" 当前EXP: "+str(UD[4])+" 下一级EXP: " + str(UD[5])+" 还需: "+str(UD[5]-UD[4])+" EXP")
            if UD[3] == "6":
                print("\n你的等级已经到LV.6级了🎉,不在执行每日基础任务"); return False
            else: return True
        except KeyError as e:
            print(f"数据缺失:{e}"); return False
        except Exception as e:
            print(f"未知错误: {e}")

    def sign_in(self, cookie:dict) -> bool:      # B站签到
        print("\n#正在进行B站签到任务#"); time.sleep(Sleeptime)
        response = Request().get([self.url['Bili_Sign'], cookie]).json()
        if response['code'] == -101:
            print("签到失败,请检查脚本😨"); return False
        else:
            print(time.strftime("%m月%d日B站签到完成") + "🥳"); return True
    
    def live_sign_in(self, cookie:dict) -> bool: # B站直播签到
        print("\n#正在进行直播签到任务#"); time.sleep(Sleeptime)
        try:
            response = Request().get([self.url["Bili_live"], cookie]).json()
            if response['code'] == 1011040:
                print("你已经签到过了明天再来吧😁")
                return True
            elif response['code'] == -101:
                print("B站直播签到失败😨")
                return False
            else:
                print("本月签到" + str(response['data']['hadSignDays']) + "次")
                print("本次签到奖励👉 " + response['data']['text'])
                return True
        except TypeError as e:
            print(f"返回数据错误:{e}")
            return False

    def exchange_silver_melon(self, data:list) -> bool: # 银瓜子兑换硬币
        print("\n#正在进行银瓜子兑换硬币#"); time.sleep(Sleeptime)
        if data[1] == False: print("\n😃 银瓜子兑换硬币配置为False,此Cookie不进行兑换"); return 
        response = Request().get([self.url['Silver_Melon'], data[0]]).json()
        if response['code'] != 0:
            print("获取瓜子数量失败😨"); return False
        else:
            response = response['data']
            print("当前有:"+ str(response['silver']) + "个银瓜子🤑")
        post_data = {
            "csrf_token": data[0]['bili_jct'],
            "csrf": data[0]['bili_jct']
            }
        response = Request().post([self.url['Silver_Exchange'], data[0], post_data]).json()
        if response['code'] == 0:
            print("兑换成功🥳")
            return True
        elif response['code'] == 403:
            print("银瓜子不够兑换失败😫 (700瓜子:1硬币)")
        else:
            print("兑换失败😨,请检查脚本")

    def get_video(self, data:list) -> list:     # 获取任务视频
        print("\n#正在进行获取任务视频#"); time.sleep(Sleeptime)
        Aid_data = []
        if data[1] is True:
            print("正在获取随机📺")
            response = Request().get([self.url['Hot_Video'], data[0]])
            if response.status_code != 200:
                print("获取📺 失败😨请检查网址是否能用");return False
            else:
                res = response.json()['data']['list']
                for i in res:
                    Aid_data.append(i['aid'])
                print("获取到"+ str(len(Aid_data)) +"个📺")
                print("获取随机📺 结束")
                return Aid_data
        else:
            print("正在获取指定up📺")
            for i in data[1]:
                url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?host_mid=" + i
                response = Request().get([url,data[0]]).json()
                if response['code'] != 0:
                    print("请求错误😨请检查线路是否能用")
                for i in response['data']['items']:
                    try:
                        Aid_data.append(i['modules']['module_dynamic']['major']['archive']['aid'])
                    except:
                        pass
            print("获取到"+ str(len(Aid_data)) +"个📺")
            print("获取指定视频结束🤪")
            return Aid_data
        
    def shave_video(self, data:list) -> bool:   # 分享视频
        print("\n#正在进行分享视频任务#"); time.sleep(Sleeptime)
        post_data = {
            "aid" : data[1][random.randint(0, len(data[1]) - 1)], 
            "csrf": data[0]['bili_jct']
            }
        response = Request().post([self.url['Shave_Video'],data[0],post_data])
        try:
            response = response.json()
            if response['code'] == 0:
                print(time.strftime("%m月%d日分享视频完成") + "🥳"); return True
            elif response['code'] == 71000:
                print("你已经分享过此视频了😫"); return False
            else:
                print(f"分享失败😨未知错误👉{response}"); return False
        except:
            print(f"分享失败😨未知错误👉{response}"); return False
    
    def look_video(self,data:list) -> bool:      # 观看视频
        print("\n#正在进行观看视频任务#"); time.sleep(Sleeptime)
        post_data = {
            "aid" : data[1][random.randint(0, len(data[1]) - 1)], 
            "csrf": data[0]['bili_jct'],
            "played_time": random.randint(33, 66)
            }
        response = Request().post([self.url['Look_Video'], data[0], post_data])
        try:
            response = response.json()
            if response['code'] == 0:
                print(time.strftime("%m月%d日观看视频完成") + "🥳"); return True
            else:
                print(f"观看失败😨未知错误👉{response}")
                return False
        except:
            print(f"观看失败😨未知错误👉{response}")
            return False

    def put_coin(self, data:list) -> bool:      # 视频投币
        print("\n#正在进行视频投币任务#"); time.sleep(Sleeptime)
        if data[3] == False: print("\n😃 投币任务配置为False,此Cookie不执行投币任务"); return True
        try:
            exp = Request().get([self.url['Get_Exp'], data[0]]).json()['data']
            coin = Request().get([self.url['Coin'], data[0]]).json()['data']['money']
            exp = 50 - exp
        except:
            print("请求数据失败😨")
        if exp == 0: print(time.strftime("%m月%d日投币任务已完成") + "🥳"); return True
        elif coin < 10: print("硬币小于10个😱,启动白嫖"); return True
        else:
            print('今日还有'+str(exp)+'📖未获得,当前有'+str(coin)+'个💿')
            print("#开始投币#"); num = 0; err = 0
            while True:
                time.sleep(Sleeptime)
                if num >= exp: print(time.strftime("%m月%d日投币任务已完成") + "🥳"); return True
                elif err >= 10: print("多次投币错误😨"); return False
                else: 
                    post_data = {
                        'aid': data[2][random.randint(0, len(data[2]) - 1)], 
                        'multiply': data[1], 
                        'select_like': 0,
                        'cross_domain': 'true', 
                        'ramval': 0,
                        'csrf': data[0]['bili_jct']
                        }
                    try:
                        response = Request().post([self.url['Put_Coin'], data[0], post_data]).json()
                        if response['code'] == 0: print("已向"+ str(post_data['aid']) +"视频投出"+ str(post_data['multiply']) +"个💿"); num += 10
                        elif response['code'] == 34005: print("你已经向"+ str(post_data['aid']) +"投过币了😫"); err += 1
                        else: err += 1; print("投币出现异常😨")
                    except:
                        print("投币请求失败😨"); return True
                
    def run():
        num = 1
        for i in user_config():
            print("\n"+"*"*10+"正在执行第" + str(num) + "个cookie"+"*"*10)
            num += 1

            if i['Work'] == False: # 检查Work是否为False
                print("😃 脚本运行配置为False,此Cookie不执行🦶 本"); continue
            else:
                level = RunTask().get_user_data(i['Cookie'])
                if i['Task'] and level:  
                    Aid_data = RunTask().get_video([i['Cookie'], i['Up']])
                    function = [
                        RunTask().live_sign_in(i['Cookie']),
                        RunTask().exchange_silver_melon([i['Cookie'], i['Exchange']]),
                        RunTask().shave_video([i['Cookie'], Aid_data]),
                        RunTask().look_video([i['Cookie'], Aid_data]),
                        RunTask().put_coin([i['Cookie'], i['Coin'], Aid_data, i['Put']])
                    ]
                else:
                    print("\n😃 基础任务配置为False,此Cookie不执行每日任务")
                    function = [
                        RunTask().live_sign_in(i['Cookie']),
                        RunTask().exchange_silver_melon([i['Cookie'], i['Exchange']])
                    ]
                    
            for i in function:
                if i == False: print("\n#运行错误#"); break
                else: print("\n#结束运行#"); break

RunTask.run()
