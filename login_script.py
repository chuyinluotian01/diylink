import json
import requests

# 读取配置文件
def read_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

# 发送PushPlus通知
def send_pushplus_notification(token, title, content):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": "txt"
    }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print(f"Failed to send notification: {response.text}")

# 登录并发送通知
def login_and_notify(account, pushplus_token):
    url = "https://console.diylink.net/api/user/auth/info"
    headers = {
        "Host": "console.diylink.net",
        "Connection": "keep-alive",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-TW",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "token": account["token"],  # 使用账户中的 token
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://console.diylink.net/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Cookie": account["cookie"]  # 使用账户中的 cookie
    }

    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Data: {response_data}")

        if response.status_code == 200:
            if response_data.get("code") == 200:  # 假设成功的状态码是200
                send_pushplus_notification(pushplus_token, f"账号 {account['username']} 登陆成功", f"账号 {account['username']} 登陆成功")
                print(f"账号 {account['username']} 登陆成功")
            else:
                encrypted_message = response_data.get("msg", "Unknown error")
                send_pushplus_notification(pushplus_token, f"账号 {account['username']} 登陆失败", f"账号 {account['username']} 登陆失败: {encrypted_message}")
                print(f"账号 {account['username']} 登陆失败: {encrypted_message}")
        else:
            send_pushplus_notification(pushplus_token, f"账号 {account['username']} 登陆失败", f"账号 {account['username']} 登陆失败: HTTP {response.status_code}")
            print(f"账号 {account['username']} 登陆失败: HTTP {response.status_code}")
    except Exception as e:
        send_pushplus_notification(pushplus_token, f"账号 {account['username']} 登陆失败", f"账号 {account['username']} 登陆失败: {str(e)}")
        print(f"账号 {account['username']} 登陆失败: {str(e)}")

def main():
    config = read_config()
    accounts = config["accounts"]
    pushplus_token = config["pushplus_token"]

    for account in accounts:
        login_and_notify(account, pushplus_token)

if __name__ == "__main__":
    main()
