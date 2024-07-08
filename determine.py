import yaml

data = yaml.load(open('./config.yml', encoding="utf-8"), Loader=yaml.FullLoader)

try:
    print("检测到填写了"+str(len(data["User_Cookie"]))+"个Cookie")
except TypeError as e:
    print("运行错误😨未填写Cookie或填写错误")

def handle_cookie():
    uData = []
    Bili_SESSDATA = []
    for i in range(0, len(data["User_Cookie"])):
        Bili_SESSDATA.append(data['User_Cookie'][i].split(',')[0])
    for i in [i.split("; ") for i in Bili_SESSDATA]:
        uData.append(dict(i.split("=", 1) for i in i))
    return uData

def user_config():
    user_config = []
    name = ['Work', 'Up', 'Task', 'Put', 'Coin', 'Exchange','Cookie']
    config_name = ['Work_Cookie', 'Appoint_Up', 'Day_Task', 'Put_Coin', 'Coin_Number', 'Exchange_Coin']
    for i in range(0, len(data["User_Cookie"])):
        cookie_config = {}
        user_config.append(cookie_config)
        cookie_config['Cookie'] = handle_cookie()[i]
        for n, cn in zip(name, config_name):
            try:
                cookie_config[n] = data[cn][i]
            except:
                cookie_config[n] = True

            if cookie_config[n] == None:
                cookie_config[n] = True

        if cookie_config['Coin'] != (2 or 1):
            cookie_config['Coin'] = 1

    return user_config