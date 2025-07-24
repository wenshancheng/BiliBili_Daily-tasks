import time
import requests_html
import random
from notify import pushplus_bot  # 青龙信息推送

Session = requests_html.HTMLSession()

IS_PUSH = False     # 是否信息推送(只兼容青龙pushplus推送)
up_uid = [  # up的uid
    ['xxx', 'xxx'],  # 第一个cookie的指定upuid
    [],  # 以此类推
]
IS_Put = [      # 是否投币
    False,
]
Put_Coin = [    # 投币数量
    1,
]

cookie = 'bwopkrdpowe=1;@1234124'  # cookie填写在此处,多个cookie用@隔开

log_info = ''


class RunTools:
    def cookie_spilt(cookie_str: str) -> list:
        parts = []
        if '@' in cookie_str:
            cookie_str = cookie_str.split('@')
        else:
            cookie_str = [cookie_str]

        try:
            for i in [i.split("; ") for i in cookie_str]:
                parts.append(dict(i.split("=", 1) for i in i))
        except:
            RunTools.push_info("cookie格式错误😓")
        return parts

    def push_info(infos: str):
        global log_info
        log_info += infos + "\n"
        print(infos)


push = RunTools.push_info


class RunTask:
    def __init__(self):
        self.api_url = "https://api.bilibili.com/x",
        self.token = ''
        self.headers = {"User-Agent": requests_html.UserAgent().random,
                        "Referer": "https://space.bilibili.com", }

    def get_user_data(self) -> bool:      # 获取用户信息
        push("#正在获取用户基本信息#")
        try:
            res = Session.get(self.api_url[0]+'/space/myinfo',
                              headers=self.headers, cookies=self.token)

            if res.status_code != 200:
                push(f"请求用户信息失败😨状态码👉 ", res.status_code)
                push(f'响应内容:{res}...')
                return False

            res = res.json()
            if res['code'] == -101:
                push("cookie错误😨请检查cookie是否正确")
                return False

            res = res['data']
            UD = []
            for key in ['name', 'mid', 'coins', 'level']:
                if key not in res:
                    push(f"😨数据缺失:{key}")
                    return False
                else:
                    UD.append(str(res[key]))

            res = res['level_exp']
            for key in ['current_exp', 'next_exp']:
                if key not in res:
                    push(f"😨数据缺失:{key}")
                    return False
                else:
                    UD.append(res[key])

            push("😀 : " + UD[0] + " mid: "+UD[1] +
                 " 当前还有硬币: " + UD[2] + "个🤑")
            push("当前🌵: "+UD[3]+" 当前EXP: "+str(UD[4])+" 下一级EXP: " +
                 str(UD[5])+" 还需: "+str(UD[5]-UD[4])+" EXP")
            if UD[3] == "6":
                push("\n你的等级已经到LV.6级了🎉,只完成签到任务")
                self.sign_in(cookie)
                return False
            else:
                return True
        except KeyError as e:
            push(f"😨数据缺失:{key}")
            return False
        except Exception as e:
            push(f"😨未知错误:{e}")

    def sign_in(self) -> bool:      # B站签到
        push("\n#正在进行B站签到任务#")
        res = Session.get(
            self.api_url[0]+'/web-interface/nav/stat', headers=self.headers, cookies=self.token).json()
        if res['code'] == -101:
            push("签到失败,请检查脚本😨")
            push(f'响应内容:{res}...')
            return False
        else:
            push(time.strftime("%m月%d日B站签到完成") + "🥳")

    def get_video(self, uid: list) -> list:     # 获取视频
        push("\n#正在B站获取视频#")
        Aid = []
        if not any(uid):
            push("正在获取随机📺")
            res = Session.get(
                self.api_url[0]+'/web-interface/popular?ps=50&pn=1', headers=self.headers, cookies=self.token)

            if res.status_code != 200:
                push(f'获取📺 失败😨，状态码：', res.status_code)
                push(f'响应内容:{res}...')
                return False

            res = res.json()['data']['list']
            for i in res:
                Aid.append(i['aid'])
            push("获取到" + str(len(Aid)) + "个📺")
            push("获取随机📺 结束")
            return Aid

        else:
            push("正在获取指定up📺")
            for i in uid:
                url = self.api_url[0] + \
                    "/polymer/web-dynamic/v1/feed/all?host_mid=" + i
                res = Session.get(
                    url, headers=self.headers, cookies=self.token).json()

                if res['code'] != 0:
                    push(f"获取📺 失败😨，状态码： {res['code']}")
                    push(f'响应内容:{res}')
                    return False

                for i in res['data']['items']:
                    try:
                        Aid.append(
                            i['modules']['module_dynamic']['major']['archive']['aid'])
                    except:
                        pass
            push("获取到" + str(len(Aid)) + "个📺")
            push("获取指定视频结束🤪")
            return Aid

    def look_video(self, aid) -> bool:      # 观看视频
        print("\n#正在进行观看视频任务#")
        post_data = {
            "aid": aid[random.randint(0, len(aid) - 1)],
            "csrf": self.token['bili_jct'],
            "played_time": random.randint(33, 66)
        }
        res = Session.post(
            self.api_url[0]+'/click-interface/web/heartbeat', headers=self.headers, cookies=self.token, data=post_data)
        try:
            res = res.json()
            if res['code'] == 0:
                push(time.strftime("%m月%d日观看视频完成") + "🥳")
                return True
            else:
                push(f"观看失败😨未知错误👉{res}")
                return False
        except:
            push(f"观看失败😨未知错误👉{res}")
            return False

    def shave_video(self, aid) -> bool:   # 分享视频
        push("\n#正在进行分享视频任务#")
        post_data = {
            "aid": aid[random.randint(0, len(aid) - 1)],
            "csrf": self.token['bili_jct']
        }
        response = Session.post(
            self.api_url[0] + '/web-interface/share/add', cookies=self.token, data=post_data)
        try:
            response = response.json()
            if response['code'] == 0:
                push(time.strftime("%m月%d日分享视频完成") + "🥳")
                return True
            elif response['code'] == 71000:
                push("你已经分享过此视频了😫")
                return False
            else:
                push(f"分享失败😨未知错误👉{response}")
                return False
        except:
            push(f"分享失败😨未知错误👉{response}")
            return False

    def put_coin(self, data: list) -> bool:      # 视频投币
        push("\n#正在进行视频投币任务#")
        if data[2] == False:
            push("\n😃 投币任务配置为False,此Cookie不执行投币任务")
            return False
        if data[1] > 2:
            push("投币最大数量为2😓")
            return False
        try:
            exp = Session.get(self.api_url[0]+'/web-interface/coin/today/exp', headers=self.headers,
                              cookies=self.token).json()['data']
            coin = Session.get("http://account.bilibili.com/site/getCoin", headers=self.headers, cookies=self.token).json()[
                'data']['money']
            exp = 50 - exp
        except:
            push("请求数据失败😨")
            return False
        if exp == 0:
            push(time.strftime("%m月%d日投币任务已完成") + "🥳")
            return True
        elif coin < 10:
            push("硬币小于10个😱,启动白嫖")
            return True
        else:
            push('今日还有'+str(exp)+'📖未获得,当前有'+str(coin)+'个💿')
            push("#开始投币#")
            num = 0
            err = 0
            while True:
                time.sleep(1)
                if num >= exp:
                    push(time.strftime("%m月%d日投币任务已完成") + "🥳")
                    return True
                elif err >= 10:
                    push("多次投币错误😨")
                    return False
                else:
                    post_data = {
                        'aid': data[1][random.randint(0, len(data[1]) - 1)],
                        'multiply': data[0],
                        'select_like': 0,
                        'cross_domain': 'true',
                        'ramval': 0,
                        'csrf': self.token['bili_jct']
                    }
                    try:
                        res = Session.post(
                            self.api_url[0]+'/web-interface/coin/add', headers=self.headers, cookies=self.token, data=post_data).json()
                        if res['code'] == 0:
                            push(
                                "已向" + str(post_data['aid']) + "视频投出" + str(post_data['multiply']) + "个💿")
                            num += 10
                        elif res['code'] == 34005:
                            push("你已经向" + str(post_data['aid']) + "投过币了😫")
                            err += 1
                        else:
                            err += 1
                            push("投币出现异常😨")
                    except:
                        push("投币请求失败😨")
                        return True

    def run(self):
        if len(cookie) != 0:
            cookies = RunTools.cookie_spilt(cookie)
            push(f"\n{10*str('#')} 共获取到👉 {len(cookies)}个账号 {10*str('#')}")
            for index, infoc in enumerate(cookies,):
                push("\n"+"*"*8+"正在执行第" + str(index+1) + "个cookie"+"*"*8)
                self.token = infoc
                level = self.get_user_data()
                if level:
                    self.sign_in()
                    aid = self.get_video(up_uid[index])
                    self.look_video(aid)
                    self.shave_video(aid)
                    self.put_coin([Put_Coin[index], aid, IS_Put[index]])
                else:
                    push("\n运行结束")
        else:
            push("未填写Cookie结束运行😓")


RunTask().run()

if IS_PUSH:
    pushplus_bot(title='B站签到推送', content=log_info)
