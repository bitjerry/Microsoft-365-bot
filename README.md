# Microsoft 365 bot

---
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Manage the Microsoft 365 Global through the telegram bot

Read in other languages: English | [简体中文](./README.zh-CN.md)

### Create a Robot

---
See @BotFather
#### Commands
```commandline
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


### Running Environment

---
```commandline
python 3.10
```

### Install

---
```commandline
git clone https://github.com/bitjerry/Microsoft-365-bot.git
cd Microsoft-365-bot
```

### Deploy

---
The program supports fly.io, heroku and vps

1. Create a PostgresSQL database

2. Create an application

3. Setting environment variables

#### Heroku: 
There is a very friendly graphical user interface for the web.

1. Create app
2. Create a PostgresSQL database for app
3. Run `public.sql` for postgres
4. Add environment variables to the app
5. Deployment Program
```commandline
git init
heroku git:remote -a xxx.git
git add .
git commit -m "Initialize Project"      
git push heroku master
```

#### Fly.io: 
You need to do this from the command line:

1. Create a PostgresSQL database for app
```commandline
flyctl postgres create to create table
```
2. Run `public.sql` for postgres
3. Create app
```commandline
flyctl launch
```
4. Attach database to app
```commandline
flyctl postgres attach --app <app-name> <postgres-app-name>
```
5. Add environment variables to the app
```commandline
flyctl secrets set BOT_TOKEN="xxx"
flyctl secrets set ADMIN_ID="xxx"
```
7. Deployment Program
```commandline
flyctl deploy
```

#### VPS

1. Prepare your database
If you don't want to use Postgres, you can try using SQLite3 in `db/db.py`.  
I have written a database core class in the py file, but I have not tested it.   
The `public.sql` file for Postgres is not applicable.  
By the way, you can write another class to replace them, such as mysql.

2. Add environment variables to the app
3. Deployment Program
```commandline
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
2. The program uses flask to implement webhook, you can use polling for local development.
3. It is important to ensure that the applications created in AZ have sufficient permissions, which APIs need which permissions to view Microsoft documents.
   >https://docs.microsoft.com/en-us/graph/api/
   
### License

---
MIT © [bitjerry](./LICENSE)
  
*2022/9/1*
*Mr.lin*