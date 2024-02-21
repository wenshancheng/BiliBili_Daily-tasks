import yaml

text = yaml.load(open('./config.yml',encoding="UTF-8"),Loader=yaml.FullLoader)

#获取并处理用户Cookie
def get_cookie():   
    Bili_SESSDATA = text['User_Cookie']
    Bili_SESSDATA = Bili_SESSDATA.split(',')
    try: 
        Bili_SESSDATA.index(''); Bili_SESSDATA.remove(''); 
        print("请正确填写cookie值😨"); return Bili_SESSDATA
    except: return Bili_SESSDATA

def handle_cookie():
    Bili_SESSDATA = get_cookie()
    cookie_dict = []; cookie_list = []
    for i in [i.split("; ") for i in Bili_SESSDATA]:
        cookie_dict.append(dict(i.split("=", 1) for i in i))
    print("检测到" + str(len(Bili_SESSDATA)) + "个cookie")
    print("按要求处理"+str(text['Cookie_Number'])+"个Cookie")
    if text['Cookie_Number'] > len(Bili_SESSDATA):
        print("请不要乱填Cookie_Number数字😡")
        return cookie_list
    else:
        for i in range(0,text['Cookie_Number']):
            cookie_list.append(cookie_dict[i])
        return cookie_list

#判断用户硬币和投币经验
def determine(exp,coin):
    if text['Coin'] == 0: print('是否投币👉 No'); return 0
    else:
        print('是否投币👉 YES')
        if exp == 0: print("已经完成视频投币任务😳"); return 0
        else:
            if coin == 0:  print("你的硬币不足已停止投币😫")
            else:
                print('今日还有'+str(exp)+'📖未获得,当前有'+str(coin)+'个硬币')
                if (exp/10) >= coin:
                    print('投出所有硬币😬')
                    return coin
                else: 
                    print('正常投币😎')
                    return int(exp/10)
def multiply():
    if text['Multiply'] > 2: print("最大就两个硬币")
    else:   return text['Multiply']

#判断是否兑换银瓜子
def exchange_silver(num) -> bool or str:
    print("当前有:"+str(num)+"个💿瓜子")
    if text['Silver'] == False: print('是否兑换银瓜子👉 No')
    else:
        print('是否兑换银瓜子👉 Yes')
        if num < 700: print("💿瓜子不足无法换硬币")
        else:
            return True
        
#获取视频aid
def get_pop_video(num) -> list:
    if text['Appoint_Up'] == True:
        print('是否指定UID👉 YES')
        data = text['Up_Uid']
        if text['Cookie_Number'] > len(text['Up_Uid']):
            try: return data[num-1][str(num)]
            except: return data[0]["1"]
        else:
            return data[num-1][str(num)]
    else:
        print('是否指定UID👉 No')
        return True
