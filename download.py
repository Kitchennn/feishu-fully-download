from time import sleep
import requests
import json
from appConfig import file_extension_relat

def createtask(file_extension,token,type,user_access_token):
    url = "https://open.feishu.cn/open-apis/drive/v1/export_tasks"
    payload = json.dumps({
        "file_extension": file_extension,
        "token": token,
        "type": type
    })
    headers = {
    'Authorization': 'Bearer ' + user_access_token,
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
    return (response.text)

def checktask(ticket,token,user_access_token):
    url = "https://open.feishu.cn/open-apis/drive/v1/export_tasks/" + ticket + "?token=" + token
    #print(url)
    payload = ''
    headers = {
    'Authorization': 'Bearer ' + user_access_token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    #print(response.text)
    return (response.text)

def downloadtask(file_token,file_path_full,user_access_token):
    url = "https://open.feishu.cn/open-apis/drive/v1/export_tasks/file/"+file_token+"/download"
    payload = ''
    headers = {
    'Authorization': 'Bearer ' + user_access_token
    }
    response = requests.request("GET", url, headers=headers, data=payload, stream=True)
    #print(response.iter_content)
    with open(str(file_path_full), 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    print("下载成功")
    return ("下载完成")

job_status_relat = {
    "0": "成功",
    "1":"初始化",
    "2":"处理中",
    "3":"内部错误",
    "107":"导出文档过大",
    "108":"处理超时",
    "109":"导出内容块无权限",
    "110":"无权限",
    "111":"导出文档已删除",
    "122":"创建副本中禁止导出",
    "123":"导出文档不存在",
    "6000":"导出文档图片过多"
}

def export2downloadthefile(file_extension,token,type,file_path,user_access_token):
    response_createtask = createtask(file_extension,token,type,user_access_token)
    sleep(1)
    ticket = json.loads(response_createtask)["data"]["ticket"]
    #print(ticket)
    response_checktask = json.loads(checktask(ticket,token,user_access_token))
    #print(response_checktask)
    #print(response_checktask["data"]["result"]["job_status"])
    while True:
        if response_checktask['data']['result']['job_status'] == 0:
            file_token = response_checktask["data"]["result"]["file_token"]
            file_path_full = file_path + "/" + response_checktask["data"]["result"]["file_name"] + "." + file_extension_relat[type]
            print(file_path_full)
            downloadtask(file_token,file_path_full,user_access_token)
            return ("下载完成")
        elif response_checktask["data"]["result"]["job_status"] in [1,2]:
            print("任务处理中")
            sleep(1)
            response_checktask = json.loads(checktask(ticket,token,user_access_token))
            continue
        else:
            print("任务失败", job_status_relat[response_checktask["data"]["result"]["job_status"]])
            return("下载失败")

def downloadthefile(file_path,file_name,user_access_token,file_token):
    url = "https://open.feishu.cn/open-apis/drive/v1/files/" + file_token + "/download"
    payload = ''
    headers = {
    'Authorization': 'Bearer ' + user_access_token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    file_path_full = file_path + "/" + file_name
    with open(str(file_path_full), 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    print("下载成功")
    return ("下载完成")
