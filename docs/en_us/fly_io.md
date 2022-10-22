### Deploy
1. Clone the project

```bash
git clone https://github.com/bitjerry/Microsoft-365-bot.git
cd Microsoft-365-bot
```
2. Create an app

```bash
flyctl launch
```
3. Setting up a Postgres database for your application
4. Add environment variables (required)
> [More optional >>>](config.md)
```bash
flyctl secrets set BOT_TOKEN="xxx"  Robot token, get by @BotFather
flyctl secrets set ADMIN_ID="xxx"   tg's user id (a string of pure numbers), usually the owner id
```
5. Deploy the application

```bash
flyctl deploy
```

##### If you don't understand, please see the picture:

<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/5.png" alt="screenshots"></p>

### Update

#### By Github Action

- Fork project
- Create environment password:
  - FLY_API_TOKEN: [Create Token](https://fly.io/user/personal_access_tokens)
  - APP_NAME: App name on fly.io
- Find the GitHub Actions button and click the `Run workflow` button