import requests
import base64
import json,random,time,os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# 读取文件
def open_file(file_path):
    #with open(file_path, 'wb+') as f:
    #    return f.read()
    #以 utf-8 的编码格式打开指定文件
    f = open(file_path,'rb+')
    #输出读取到的数据
    return f.read()
    #关闭文件
    

# 将文件转换为base64编码，上传文件必须将文件以base64格式上传
def file_base64(data):
    data_b64 = base64.b64encode(data).decode('utf-8')
    #print(data_b64)
    return data_b64

def random_file_name():
    #随机生成一串字符
    name = ""
    for i in range(0,15):
        a = random.choice('abcdefghijklmnopqrstuvwxyz')
        name = name+a
    name= name+str(int(time.time()))
    return name
        

# 上传文件
def upload_files(file_data,file_name):
    houzhui = os.path.splitext(file_name)[-1] #获取文件后缀
    file_name = random_file_name()+houzhui #文件名
    token = ""#填写github token
    url = "https://api.github.com/repos/mikulo/img/contents/img/"+file_name  # 用户名、库名、路径
    headers = {"Authorization": "token " + token}
    content = file_base64(file_data)
    data = {
        "message": "message",
        "committer": {
            "name": "mikulo",
            "email": "test@gmail.com"
        },
        "content": content
    }
    data = json.dumps(data)
    req = requests.put(url=url, data=data, headers=headers)
    req.encoding = "utf-8"
    re_data = json.loads(req.text)
    #print(re_data)
    #print(re_data['content']['sha'])
    return "https://i2.wp.com/raw.githubusercontent.com/mikulo/img/master/img/"+file_name #这里添加了wordpress的免费图片代理


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'

@app.route('/upload')
def upload_file():
    return render_template('upload.html')#初始页面

@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        file = f.read()
        #print(f.filename) #f.filename为文件名
        link0= upload_files(file,f.filename)#调用上传函数并返回图片链接
        #print(request.files)
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        link1= "[img]"+link0+r'[/img]' #生成ubb链接
        return render_template('upload.html',url_0=link0,url_1=link1)#跳转到初始界面并将链接传入

    else:

        return render_template('upload.html',url_0=link0,url_1=link1)

if __name__ == '__main__':
   app.run(host="0.0.0.0",debug=True)
'''
#以下为测试本地文件上传代码，无视即可
if __name__ == '__main__':
    file_name='1.jpg'
    fdata = open_file(file_name)
    #print(file_name)
    #print(str(fdata))
'''
