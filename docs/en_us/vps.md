1. Prepare a database, any database
2. Make sure the python version is above 3.10
3. Clone to local

```bash
git clone https://github.com/bitjerry/Microsoft-365-bot.git
cd Microsoft-365-bot/src
```
4. Add environment variables (required)
> [More optional >>>](config.md)
```bash
flyctl secrets set BOT_TOKEN="xxx"  Robot token, get by @BotFather
flyctl secrets set ADMIN_ID="xxx"   tg's user id (a string of pure numbers), usually the owner id
```
3. Deployment procedure:

```bash
pip install -r requirements.txt
python3 setup.py
```