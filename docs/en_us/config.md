## Configuration file (environment variables)
```
./config.py
```
### Required
#### BOT_TOKEN
Type: String
> Telegram robot token, available at @BotFather
#### ADMIN_ID
Type: Int
> The id of telegram bot user. It is believed that no one wants to share private property with others.

### Suggest
#### WEBHOOK_URL
Type: String
> Set up a webhook link that will allow your application to listen to the telegram server instead of pulling messages from it  
> This option will enable the webhook mode. Otherwise, the default mode is polling   
> It is recommended to fill this in, just fill in a url *https://.* (note: must be https)  
#### BOT_LANG
Type: String
> The robot user interface supports multiple languages, the default is American English `en_us`. Optional Simplified Chinese `zh_cn`  
> For details, see `./resource/i18n`  
[>>> Localization development](dev.md)

### Optional
#### PORT
Type: Int
> The program's listening port, valid only when webhook is enabled  
> The default value is `5000`. On heroku, the free port is not optional. fly.io is `8080`
#### DATABASE_URL
Type: String
> If you are using a serverless such as heroku or fly.io and has attached a postgres database to it, leave this parameter unfilled  
> If you are deploying on VPS, please refer to the specification for different data sources  
> https://docs.sqlalchemy.org/en/14/core/engines.html  
#### SECRET
Type: String
> Operation password, which is provided when manipulating sensitive data  
> If you need more security, you can choose to set this password, and then if you fill in sensitive operations will ask you to enter the password  
> It is disabled by default, that means there is no password that need to be entered when you're operating the robot   
> [>>> Learn more about security](security.md)
#### SECRET_TIMES
Type: Int
> This parameter is valid only when `SECRET` is set.  
> Maximum number of password retries. Sensitive operations will be locked if this number is exceeded. You can try to restart the service  
> The default value is `-1` with no limit on the number of errors.  

#### WELCOME_URL
Type: String
> Welcome page path, which is valid only when webhook mode is enabled, to check whether webhook is enabled.  
> The path is a relative path. If this parameter is not specified, the root path is `/` by default  
> If you do not want the program to be scanned, it is recommended to change
#### EXPIRE_KEY
Type: Int
> App encryption key display time, after the expiration will be hidden, no longer visible  
> The default value is `300` seconds
#### EXPIRE_LOGS
Type: Int
> The unit is second  
> The default log expiration time is 30 days. After the expiration, the system automatically pushes a copy to the client and clears logs  
> `-1` Never expires
#### DEBUG
Type: Boolean
> Whether to enable debug mode. Default is `False`.  
> If you want local debugging, you can change this to `True`.  
> Do not enable debug mode in release program.   
>
> **Debug mode**  
> - Program errors are logged  
> - When a request is made to a Microsoft server, request header, request parameters, request url ars logged  
> - When requesting data from the database, the sql statement is logged  
> - When sending a request to Telegram server, request url, request body are logged  
> 
> **Release Mode**:  
> - Program errors are logged  
> - Each connection from webhook is logged, while the polling record is not logged  
> 