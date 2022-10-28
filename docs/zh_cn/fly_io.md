### 部署
1. 将项目克隆到本地
```bash
git clone https://github.com/bitjerry/Microsoft-365-bot.git
cd Microsoft-365-bot
```
2.  创建一个应用
```bash
flyctl launch
```
3. 为应用附加 Postgresql 数据库
```bash
flyctl postgres attach --app app_name db_name #app_name 应用名字, db_name 数据库名字
```
4. 添加环境变量 (必填)
> [更多选择 >>>](config.md)
```bash
flyctl secrets set BOT_TOKEN="xxx"  #机器人token, 通过@BotFather获取
flyctl secrets set ADMIN_ID="xxx"   #tg的用户id (一串纯数字), 谁使用就填谁的
```
5. 部署应用
```bash
flyctl deploy
```

##### 有不明白的请看图:

<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/5.png" alt="screenshots"></p>

### 更新

#### 通过Github Action更新

- Fork 项目
- 创建环境密码:
  - FLY_API_TOKEN: [创建Token](https://fly.io/user/personal_access_tokens)
  - APP_NAME: 在fly.io上的app名字
- 找到GitHub Actions按钮, 点击`Run workflow`按钮