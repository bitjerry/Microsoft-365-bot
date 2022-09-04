# Microsoft 365 bot

---
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

通过 telegram 机器人管理你的众多全局

使用其他语言阅读：[English](./README.md) | 简体中文

### 创建一个机器人

---
@BotFather
#### 机器人指令
```commandline
start -开始机器人
log -获取机器人运行日志
myapp -指定一个app
newapp -新建一个app
getorg -获取组织信息
getrole -获取角色信息
getsub -获取订阅信息
getuser -获取用户信息
getuserbyname -获取用户信息(通过用户名指定用户)
searchuser -获取用户信息(通过用户名模糊搜索)
adduser -添加一个用户
cancel -取消当前操作
```


### 运行环境

---
```commandline
python 3.10
```

### 安装

---
```commandline
git clone https://github.com/bitjerry/Microsoft-365-bot.git
cd Microsoft-365-bot
```

### 部署

---
程序支持 fly.io, heroku 和 vps

#### Heroku: 
大部分操作都可以在它们的页面上直接鼠标点击完成

1. 创建一个应用
2. 为应用添加一个Postgres附件
3. 运行 `public.sql`
4. 添加heroku的环境变量
5. 部署程序: 
```commandline
git init
heroku git:remote -a xxx.git
git add .
git commit -m "Initialize Project"      
git push heroku master
```

#### Fly.io: 
必须使用他们的命令行操作:

1. 创建一个Postgres应用
```commandline
flyctl postgres create to create table
```
2. 运行 `public.sql`
3. 创建一个应用
```commandline
flyctl launch
```
4. 将postgres数据库附加到应用中
```commandline
flyctl postgres attach --app <app-name> <postgres-app-name>
```
5. 为应用添加环境变量
```commandline
flyctl secrets set BOT_TOKEN="xxx"
flyctl secrets set ADMIN_ID="xxx"
```
7. 部署应用
```commandline
flyctl deploy
```

#### VPS

1. 准备好一个数据库, 当然 Postgres 并不是唯一选择.  
   好消息是, 我在`db/db.py`中提供了 *SQLite3* 的核心类用以替换, 不要在heroku或者fly.io中使用这些内存数据库  .
   坏消息是, 我并没有测试它, 但是仿写一个类应该很简单, 比如你可以写一个支持mysql的核心类
2. 不要忘记为程序添加环境变量
3. 部署程序:
```commandline
pip install -r requirements.txt
python3 setup.py
```

### 运行

---
如果是webhook直接访问 /set_webhook, 停用为 /stop_webhook

### 注意

---
1. 程序有两种模式: debug 和 release. 模式切换在 `config.py` 中的 `DEBUG = True`.  
   请注意: 在 release 模式下, db下用于加解密的rsa公私钥会在部署后自动删除
2. 程序使用 flask 实现了 webhook, 在开发环境下你可以用 polling.
3. 务必保证在az创建的应用已经给够权限, 哪些api需要哪些权限可以查看微软文档
   >https://docs.microsoft.com/en-us/graph/api/

### 许可证

---
MIT © [bitjerry](./LICENSE)
  
*2022/9/1*
*Mr.lin*