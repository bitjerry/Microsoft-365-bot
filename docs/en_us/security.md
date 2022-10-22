### Safety protection

#### 1. Database

The three parameters of the key `"client_id", "client_secret", "tenant_id"` are encrypted.   

The encryption and decryption key used asymmetric encryption in the first version. But later I considered that this is unnecessary, because the encryption and decryption are at the server.

Symmetric encryption is used in the new version, and access the key by the telegram client.

This change started in version 2.0. Sorry, I don't plan to be compatible with the previous version. The new version can no longer decrypt the previous database, please empty them and generate a new key.

#### 2. Telegram Client

Use the form of an operation password to verify the identity when performing sensitive operations. It is not turned on by default unless the user adds the password to environment variables. 

What is a sensitive operation? Add, delete, modify and check the user's information, regenerate the key, delete the domain name.

#### 3. Welcome Page

Although the program is C/S architecture, in order to avoid unknown risks, it is recommended to modify the welcome url, which can specify the path by environment variables.

### Risk

The overall security is based on the premise that the server is not stolen, and the security of Microsoft services, the security of Telegram client.

#### Server  stolen

Risk 100%. Let's not talk about what means are there for the python sandbox. As long as there is a Trojan horse to monitor incoming and outgoing traffic, the service program has no security at all. The request token to the Microsoft server is carried in the request header, and the three identification parameters of the app are passed by the get parameter. All are sent in plain text. This is the regulation of Microsoft services, and we cannot change it. By hijacking Telegram inbound traffic, sensitive information can also be modified.

How safe is the serverless account theft? fly.io do much better than heroku. The fly.io environment variables users cannot see plain text, database url are only displayed once, and extranet access requires traffic forwarding.

#### Only environment variables were stolen
Risk 0%

#### Only the database is stripped.
Risk 0%

#### Telegram account only stolen
If you set the operation password, and remove some sensitive information generated in the operation procedure in time, such as the account password. So the risk is 0% 

if you don't have an operating password, then it's 100% if you have an operating password, and some sensitive information is still left on the telegram account, then there's a risk anyway, please disable the program as soon as you find it stolen.

#### Database and Telegram account stolen
If you set the operation password and clear the sensitive information generated in some operation procedures in time, there will still be no risk.

### Key usage
When the program starts, it will first automatically detect whether there is data in the database. If there is, please enter the existing key to decrypt them. Otherwise, please request a new key, which will clear all the data that cannot be decrypted and empty the database.

**Be sure to protect the key and operating password ❗❗❗**  

**Be sure to protect the key and operating password ❗❗❗**  

**Be sure to protect the key and operating password ❗❗❗**
