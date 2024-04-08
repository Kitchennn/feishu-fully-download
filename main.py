import requests
import json
from appConfig import APP_ID,APP_SECRET,REDIRECT_URI,SCOPE,STATE,root_folder,file_extension_relat
import os
from download import export2downloadthefile,downloadthefile
#获取tenant_access_token
def get_tenant_access_token(app_id,app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": app_id,
        "app_secret": app_id
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    #print("tenant_access_token = ",response.text)
    return(response.text)

#获取app_access_token
def get_app_access_token(app_id,app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    payload = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret
    })


    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print("app_access_token = ",response.text)

#获取user_access_token
def get_user_access_token(code,app_access_token):
    url = "https://open.feishu.cn/open-apis/authen/v1/oidc/access_token"
    payload = json.dumps({
        "code": "xMSldislSkdK",
        "grant_type": "authorization_code"
    })


    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    #print("user_access_token = ",response.text)
    return(response.text)

#获取授权登录授权码
def get_user_auth_code(APP_ID,REDIRECT_URI,SCOPE,STATE):
    url = "https://open.feishu.cn/open-apis/authen/v1/authorize?app_id=" + APP_ID + "&redirect_uri=" + REDIRECT_URI + "&scope=" + SCOPE + "&state" + STATE
    # 	https://open.feishu.cn/open-apis/authen/v1/authorize?app_id={APPID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}&state={STATE}

    response = requests.request("GET", url)
    #print("登录授权 = ",response.text)
    return(response.text) 

#获取根目录
def get_root_folder(tenant_access_token):
    url = "https://open.feishu.cn/open-apis/drive/explorer/v2/root_folder/meta"

    headers = {
    'Authorization': 'Bearer ' + tenant_access_token
    }

    response = requests.request("GET", url, headers=headers)
    #print("获取根目录",response.text)
    return(response.text) 

#获取文件夹下的清单
def get_file_list(user_access_token, page_size, page_token, folder_token, order_by, direction):
    url = "https://open.feishu.cn/open-apis/drive/v1/files?"
    if page_size:
        url = url + "page_size=" + page_size
    if page_token:
        url = url + "&page_token=" + page_token
    if folder_token:
        url = url + "&folder_token=" + folder_token
    if order_by:
        url = url + "&order_by=" + order_by
    if direction:
        url = url + "&direction="+ direction
    #print("url = ",url)

    headers = {
    'Authorization': 'Bearer ' + user_access_token
    }

    response = requests.request("GET", url, headers=headers)
    #print(response.text)
    return(response.text)

#创建文件夹
def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Folder '{directory}' created successfully.")
        else:
            print(f"Folder '{directory}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("开始干活")
    print("获取用户授权")

    #获取tenant_access_token
    #tenant_access_token = get_tenant_access_token(APP_ID,APP_SECRET)
    #tenant_access_token = 't-g10448ePVBSK6VHZVZ62RWL675WBL6YNMJBZUWVY'    #临时token

    #获取app_access_token
    #app_access_token = get_app_access_token(APP_ID,APP_SECRET)

    #获取user_access_token
    #user_access_token = get_user_access_token(get_user_auth_code(APP_ID,REDIRECT_URI,SCOPE,STATE),app_access_token)
    user_access_token = "u-eSt6YiR3N1Jp3aT0S4dpo7ll0B51g0d9Na0004Ky20j3"    #临时token

    #获取根目录
    #print("获取根目录",get_root_folder(tenant_access_token))

    #获取根目录文件清单
    #print("获取根目录文件清单",get_file_list(user_access_token, page_size = None, page_token = None, folder_token = None, order_by = "EditedTime", direction = "DESC"))

    #创建根目录
    print("创建根目录,地址为： ", root_folder)
    create_folder(directory = root_folder)

    #开始历遍多层文件夹
    #创建第一层文件夹清单数组
    print("开始历遍多层文件夹-创建文件夹清单数组")
    root_folder_list = json.loads(get_file_list(user_access_token, page_size = None, page_token = None, folder_token = None, order_by = "EditedTime", direction = "DESC"))["data"]["files"]
    #print(root_folder_list)
    folder_path_list = []
    for i in root_folder_list:
        if i["type"] == "folder":
            #print(i["name"])
            #print(i["token"])
            #创建第二层文件夹清单数组
            folder_path_list.append({"address":root_folder + "/" + i["name"], "name":i["name"], "token":i["token"]})
    #print(folder_path_list)

    #历遍第二层+文件夹
    for i in folder_path_list:
        #print("地址为： ", i["address"])
        #print("token为： ", i["token"])
        #创建第二层文件夹清单数组
        folder_path_list_temp = json.loads(get_file_list(user_access_token, page_size = None, page_token = None, folder_token = i["token"], order_by = "EditedTime", direction = "DESC"))["data"]["files"]
        for j in folder_path_list_temp:
            if j["type"] == "folder":
                #print(j["name"])
                #print(j["token"])
                #创建第三层文件夹清单数组
                folder_path_list.append({"address":i["address"] + "/" + j["name"], "name":j["name"], "token":j["token"]})
    print("完成文件夹历遍", folder_path_list)
    
    #创建文件夹
    for i in folder_path_list:
        #print("创建文件夹： ", i["address"])
        create_folder(directory = i["address"])
    print("完成文件夹创建")

    file_count = 0
    #开始下载文件
    #下载root文件夹下的文件
    for i in root_folder_list:
        if i["type"] in ["doc", "sheet", "bitable", "docx"]:
            print("开始下载文件： ", i["name"], i["token"])
            #下载文件
            export2downloadthefile(file_extension_relat[i["type"]],i["token"],i["type"],root_folder,user_access_token)
            file_count = file_count + 1
        elif i["type"] == "file":
            print("开始下载文件： ", i["name"], i["token"])
            #下载文件
            downloadthefile(root_folder,i["name"],user_access_token,i["token"])
            file_count = file_count + 1
    #下载其余文件夹的文件
    for i in folder_path_list:
        print("开始历遍文件夹： ", i["address"])
        #获取文件夹下的清单
        processing_folder_file_list = json.loads(get_file_list(user_access_token, page_size = None, page_token = None, folder_token = i["token"], order_by = "EditedTime", direction = "DESC"))["data"]["files"]
        print(processing_folder_file_list)
        for j in processing_folder_file_list:
            if j["type"] in ["doc", "sheet", "bitable", "docx"]:
                #print("开始下载文件： ", j["name"], j["token"])
                #下载文件
                export2downloadthefile(file_extension_relat[j["type"]],j["token"],j["type"],i["address"],user_access_token)
                file_count = file_count + 1
            elif j["type"] == "file":
                #print("开始下载文件： ", j["name"], j["token"])
                #下载文件
                downloadthefile(root_folder,j["name"],user_access_token,j["token"])
                file_count = file_count + 1

    print("完成下载文件,共下载了", file_count, "个文件")