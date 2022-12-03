# <a href=""><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/4.ico" align="left" height="48" width="48" ></a> Microsoft 365 bot


[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

通过 telegram 机器人管理你的众多全局账户

使用其他语言阅读：[English](/README.md) | 简体中文

**功能**
- 同时管理多个Microsoft 365全局账户
- 批量添加, 导出app
- 对用户增删查改
- 查看订阅信息, 为用户分配, 撤销订阅
- 查看组织信息
- 查看角色信息, 为用户分配, 撤销角色
- 对域名的添加与删除
- 多语言适配
- 在Microsoft Graph API中的功能未来会陆续添加

---
### 🎉演示

---
<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/bot/start.png" alt="screenshots"></p>

[👉查看更多截图 >>>](docs/zh_cn/bot.md)


### 🚀创建应用

---
>https://aad.portal.azure.com

<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/1.png" alt="screenshots"></p>
<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/2.png" alt="screenshots"></p>

#### 授予权限

---
> Organization.Read.All, Organization.ReadWrite.All  
> RoleManagement.Read.Directory, RoleManagement.ReadWrite.Directory  
> User.Read.All, User.ReadWrite.All  
> Directory.Read.All, Directory.ReadWrite.All  
> Directory.AccessAsUser.All

### 🤖创建机器人

---
<a href="https://t.me/BotFather">@BotFather</a>

<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/3.png" alt="screenshots"></p>


#### 机器人指令
```
start -开始机器人
log -获取机器人运行日志
key -保护app数据
myapp -指定一个app
newapp -新建一个app
addapps -批量添加app
exportapps -批量导出app
clearapp -清除所有app
adduser -添加一个用户
getuser -获取所有用户
getuserbyname -获取用户通过完整用户名
searchuser -获取用户通过用户名模糊搜索
listdomain -列出并管理域名
adddomain -添加一个域名
getorg -获取组织信息
getrole -获取角色信息
getsub -获取订阅信息
cancel -取消当前操作
```

### ⚙️配置参数

---
> 考虑到一键部署的方式, 配置全部采用环境变量形式  

[❓参数说明 >>>](docs/zh_cn/config.md)

### 🥼环境

---
- 数据库: 关系型数据库
- python 3.10


### 🔨部署

---
#### Heroku部署:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### 其它:

[❓Fly.io部署教程 >>>](docs/zh_cn/fly_io.md)

[❓VPS部署教程 >>>](docs/zh_cn/vps.md)

[❓Docker部署教程 >>>](docs/zh_cn/docker.md)

### 🏃运行

---
机器人有两种运行模式, 均不需要手动激活

1. *webhook*: 如果在环境变量中填入了webhook链接便自动启用
2. *polling*: 如果没有配置webhook链接, 便自动使用此方式

> 建议使用 *webhook* 因为 *polling* 会不断向telegram服务器拉取消息, 相对而言会更消耗资源

### 📝更新日志

- 2.0
  - 优化项目结构
  - 通过ORM兼容多类数据库
  - 更新数据库加密方式
  - 添加操作密码保护
  - 取消`webhook`需要手动启动
  - 启动方式自动选择
  - 对域名的操作
  - 对app的批量添加与删除
- 2.1
  - 修复bug
- 2.2
  - 添加对用户的禁用/启用
- 2.3
  - 完善对安全密钥的管理
  - 完善英文文档
  - 添加程序界面展示图
  - 修复用户列表串号问题
  - 优化代码, 及更详细的注释
- 2.4
  - 修复fly.io通过GitHub Action部署的bug
- 2.5
  - 修复数据库创建检测的bug
  - 修复对app信息修改的bug
  - 添加对docker部署的支持

### 📖更多资料

- [安全保护](docs/zh_cn/security.md)
- [开发文档](docs/zh_cn/dev.md)
- [常见问题](docs/zh_cn/error.md)

### ⚖️许可证

---
MIT © [bitjerry](/LICENSE)
  
*2022/9/1*
*Mr.lin*
