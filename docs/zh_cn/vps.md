1. 准备好一个数据库, 任意数据库
2. 确保python版本在3.10以上
3. 克隆到本地
```bash
git clone https://github.com/bitjerry/Microsoft-365-bot.git
cd Microsoft-365-bot/src
```
4. 添加环境变量 (必填)
> [更多选择 >>>](config.md)
```bash
flyctl secrets set BOT_TOKEN="xxx"  机器人token, 通过@BotFather获取
flyctl secrets set ADMIN_ID="xxx"   tg的用户id (一串纯数字), 谁使用就填谁的
```
3. 部署程序:
```bash
pip install -r requirements.txt
python3 setup.py
```