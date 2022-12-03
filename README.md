# <a href=""><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/4.ico" align="left" height="48" width="48" ></a> Microsoft 365 bot


[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Manage the Microsoft 365 Global by the telegram bot

Read in other languages: English | [简体中文](README.zh_cn.md)

**Features**
- Manage multiple Microsoft 365 global accounts by the bot
- Batch add or export apps
- Add or delete domain names
- Add, delete, check or modify users
- View subscription information, assign or revoke licenses for users
- View organization information
- View role information, assign or revoke roles for users
- Multilingual adaptation
- Functions in Microsoft graph API will be added in the future


---
### 🎉Preview

---
<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/bot/start.png" alt="screenshots"></p>

[👉More screenshot >>>](docs/en_us/bot.md)

### 🚀Create app

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
> Directory.AccessAsUser.All

### 🤖Create a Robot

---
<a href="https://t.me/BotFather">@BotFather</a> 

<p align="center"><img src="https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/3.png" alt="screenshots"></p>
 

#### Commands
```
start - Start Robot
log - Get the log of the robot
key -Protect app data
myapp - Specify an app
newapp - Create a new app
clearapp - Clear all app
addapps - Add more apps
exportapps - Batch add app
listdomain - List and manage domain names
adddomain - Add a domain name
getorg - Get organization information
getrole - Get role information
getsub - Get subscription information
getuser - Get user information
getuserbyname - Gets user information (specifies user by username)
searchuser - Get user information (by fuzzy search with username)
addUser - Add a user
cancel - Cancel the current operation
```

### ⚙️Config

---
> Considering one-button deployment, configurations are all in the form of environment variables.   

[❓Instructions >>>](docs/en_us/config.md)

### 🥼Runtime

---
- Database: SQL
- python 3.10


### 🔨Deploy

---
#### Heroku Deploy:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### Others:

[❓Fly.io >>>](docs/en_us/fly_io.md)

[❓VPS >>>](docs/en_us/vps.md)

[❓Docker >>>](docs/en_us/docker.md)

### 🏃Run

---
The bot has two modes of work and does not require manual activation.

1. *webhook*: automatically enabled if a webhook link is configured in an environment variable
2. *polling*: Use this method automatically if you do not configure a webhook link

>We recommend using *webhook* because *polling* constantly pulls out messages to the telegram server, which is relatively resource intensive

### 📝Changelog

- 2.0
  - Optimize project structure
  - Compatible with all kinds of databases through ORM
  - Update database encryption mode
  - Add operation password protection
  - The operation of manually enabling `webhook` is canceled
  - Automatic selection of startup mode
  - Operation on domain name
  - Batch addition and deletion of apps
- 2.1
  - Fix bug
- 2.2
  - Add disable/enable function for users
- 2.3
  - Improve the management of security keys
  - Improve English documents
  - Add user interface preview
  - Fixed the user module data inconsistency bug
  - Optimized code structure, and more detailed comments
- 2.4
  - Fix the bug deploy on fly.io by GitHub Action
- 2.5
  - Fix the bug for table creating
  - Fix the bug that modify app information
  - Add the support for docker

### 📖More

- [Security](docs/en_us/security.md)
- [Document](docs/en_us/dev.md)
- [FAQ](docs/en_us/error.md)

### ⚖️License

---
MIT © [bitjerry](/LICENSE)
  
*2022/9/1*
*Mr.lin*
