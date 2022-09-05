# <a href=""><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/4.ico" align="left" height="48" width="48" ></a> Microsoft 365 bot


[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Manage the Microsoft 365 Global through the telegram bot

Read in other languages: English | [简体中文](/README.zh-CN.md)

### Create app

---
>https://aad.portal.azure.com

<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/1.png" alt="screenshots"></p>
<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/2.png" alt="screenshots"></p>

### Permissions

---
> Organization.Read.All, Organization.ReadWrite.All  
> RoleManagement.Read.Directory, RoleManagement.ReadWrite.Directory  
> User.Read.All, User.ReadWrite.All  
> Directory.Read.All, Directory.ReadWrite.All  

### Create a Robot

---

<a href="https://t.me/BotFather">@BotFather</a> 

<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/3.png" alt="screenshots"></p>
 

#### Commands
```
start - Start Robot
log - Get the log of the robot
myapp - Specify an app
newapp - Create a new app
getorg - Get organization information
getrole - Get role information
getsub - Get subscription information
getuser - Get user information
getuserbyname - Gets user information (specifies user by username)
searchuser - Get user information (by fuzzy search with username)
addUser - Add a user
cancel - Cancel the current operation
```


### Python Runtime

---
```bash
python 3.10
```

### Install

---
```bash
git clone https://github.com/bitjerry/Microsoft-365-bot.git
cd Microsoft-365-bot
```

### Deploy

---

1. Create a PostgresSQL database

2. Create an application

3. Setting environment variables

#### Heroku: 


[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### Fly.io: 
You need to do this from the command line:

1. Create a PostgresSQL database for app
```bash
flyctl postgres create to create table
```
2. Create app
```bash
flyctl launch
```
3. Attach database to app
```bash
flyctl postgres attach --app <app-name> <postgres-app-name>
```
4. Add environment variables to the app
```bash
flyctl secrets set BOT_TOKEN="xxx"
flyctl secrets set ADMIN_ID="xxx"
```
5. Deployment Program
```bash
flyctl deploy
```

#### VPS

1. Prepare your database
If you don't want to use Postgres, you can try using SQLite3 in `db/db.py`.  
I have written a database core class in the py file, but I have not tested it.
By the way, you can write another class to replace them, such as mysql.

2. Add environment variables to the app
3. Deployment Program
```bash
pip install -r requirements.txt
python3 setup.py
```

### Run

---
If it is webhook just access /set_webhook, stop using /stop_webhook

### Note

---
1. The program has two modes: debug and release. Mode switch in config.py `DEBUG = True`.  
   The public and private keys of RSA will be deleted in release mode, please note that.  
2. Some serverless may sleep regularly. **Make sure to generate RSA key pairs before deployment!!!** (in the. /db directory) 
   or keep server awake, otherwise the state will be reset after hibernation and the key pair will be lost.
3. The program uses flask to implement webhook, you can use polling for local development.
4. It is important to ensure that the applications created in AZ have sufficient permissions, which APIs need which permissions to view Microsoft documents.
   >https://docs.microsoft.com/en-us/graph/api/
   
### License

---
MIT © [bitjerry](/LICENSE)
  
*2022/9/1*
*Mr.lin*
