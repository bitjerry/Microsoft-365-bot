# Development Documentation

### Get all commands from the robot


```python
# core.py
def cmd(self, command: str | Callable = ""):
    print(command)
    ...
```

### Subscribe to display beautification

> ./resource/name_for_sub.csv  
> [Download](https://learn.microsoft.com/en-us/azure/active-directory/enterprise-users/licensing-service-plan-reference)

### Localization

[Translate file >>>](../../src/resource/i18n/en_us.py)

Steps:

- Create a new `.py` file in the `i18n` directory. For the file name naming convention [Language code table](#Language-code-table)
- Translate the string against an existing file
- Variable name, `{}` string, keyboard (the dict of control) label (dict key) prohibit translation

### Main module

> The service module function is built on the app module  
> There is not a one-to-one correspondence between the app module and the service module

#### App module

> Each app module corresponds to a Microsoft Graph API module

- Create a new module in the `app` directory, the template is as follows:

```python
from util.request import *


class ModuleName(MsRequest):

    def __init__(self, request: Requests):
        super().__init__(request)
    
    def method(self, *args, **kwargs):
        self.req.get(...)
```
- Each module must inherit [MsRequest](#msrequest)
- Microsoft API usage reference
[Microsoft API](https://learn.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0) | [API Tool](https://developer.microsoft.com/zh-cn/graph/graph-explorer)
- Call method: `app.ModuleName.method()`  
Example: [Create User]( https://docs.microsoft.com/en-us/graph/api/user-post-users?view=graph-rest-1.0&tabs=http)

```python
# Microsoft document:
"""
POST https://graph.microsoft.com/v1.0/users
Content-type: application/json

{
  "accountEnabled": true,
  "displayName": "Adele Vance",
  "mailNickname": "AdeleV",
  "userPrincipalName": "AdeleV@contoso.onmicrosoft.com",
  "passwordProfile" : {
    "forceChangePasswordNextSignIn": true,
    "password": "xWwvJ]6NMw+bWH-d"
  }
}
"""
# App:
def create(self, username: str, password: str):
    """
    :param password: user password
    :param username: xxx@domain.com
    :return:
    """
    display_name = username.split('@', 1)[0]
    json = {
        'accountEnabled': True,
        'displayName': display_name,
        'mailNickname': display_name,
        'passwordPolicies': 'DisablePasswordExpiration, DisableStrongPassword',
        'passwordProfile': {
            'password': password,
            'forceChangePasswordNextSignIn': True
        },
        'userPrincipalName': username,
        'usageLocation': 'CN'
    }
    res = self.req.post(url="/users", json=json)
    return res.json["id"]

#Service:
@bot.cmd("newuser")
@app_autowired
def create(msg: Message, app: App):
    app.User.create(username)
    ...
```


#### Service Module

> Each service module corresponds to a type of Telegram bot function  
> Tool method: [helper >>>](#helper)  
> Core components: [core >>>](#core)

- Create a new module in the `service` directory
- Persistence of data
  - Create a new `session = Session()`, the session information must be initialized within `__init__`
  - Register `session_util.register(session)`
- Decorator

    ```python
    #Register bot commands
    @bot.cmd("get")
    def get_cmd(msg: Message):
        ...
    
    #Register a callback function that can take a function identity string as an argument
    @bot.callback
    def get(msg: CallbackQuery):
        ...
    
    #Inject an app Object
    @bot.cmd("adduser")
    @app_autowired
    def add_cmd(msg: Message, app: App):
        ...
    
    #Triggered when the bot starts
    @bot.on_startup
    def start():
        ...
    ```
- Keyboard

    ```python
    buttons = [[Btn(text=text,
                    callback_data=callback_data,
                    callback_func=function)]]
    bot.send_msg(msg, Text.xxx, Keyboard(buttons))
    
    # text: displays the text for the button
    # callback_data: is the data returned after the button is triggered. If you use the list for multiple parameters, the callback data is still the list
    # callback_func: is the callback function that is triggered after the button is triggered (must be registered in advance) and can identify a string for the function
    # buttons: are a two-dimensional array with columns in the first dimension and rows in the second
    ```
- Message  
    > Reference [ pyTelegramBotAPI ](https://github.com/eternnoir/pyTelegramBotAPI)

    ```python
    edit_msg(msg, text, keyboard, **keyword)
    send_msg(msg, text, keyboard, **keyword)
    send_doc(msg, doc, keyboard, **keyword)
    register_next_step(func, *args, **kwargs)
    ```
- Cross-module calls (try not to have mutual calls)
   - Information transfer
     - Pass across modules `field`, `session_util.get(field)`
   - Callback method
     - Use string to represent method name


### Util module

### MsRequest

Initiate a request

```python

def get(url: str, headers: dict, params: dict) -> Response:
    ...

def post(url: str, headers: dict, params: dict, data: dict, json) -> Response:
    ...

def delete(url: str, headers: dict) -> Response:
    ...

def patch(url: str, headers: dict, data: dict, json) -> Response:
    ...
```
Response data
-  `ok` status code, note that an exception will be thrown if the request is unsuccessful
-  `text` text for response body
-  `json` json format response data

#### helper
> Provides easy-to-use tools for service module methods

- `session_util`:
  > Manage subsessions for each module under the service
  - get():
    - Function: Used to get session parameters across modules
    - Parameters:
      - Var: Session field
  - set():
    - Function: Used to modify session parameters across modules (use with caution, may break data consistency)
    - Parameters:
      - Var: Session field
      - Value: Modified value
  - register():
    - Function: Register a session instance
    - Usage: Register(session())
  - reset():
    - Function: Reset all sessions, this time causing the bot to show no corresponding objects
  
- `task`:
  > Daemon thread for executing all deferred tasks such as timers
- clear():
  - Function: Clear all tasks
- cancel(name):
  - Function: Clear the specified task
  - Parameter: Task name
- delay(time_out, loop, name)
  - Function: Register a delayed task
  - Usage: As a decorator
  - Parameters:
    - time_out: Delayed Events
    - Loop: Whether to loop
    - Name: Task name

- `Format`:
  - Function: json data to yaml style html string
  - Usage: str (Format (json))

- `lock`:
  - Function: After setting the operation password, the user needs to check the password of the decorated function
  - Usage: As a decorator to lock the function, must be after the bot decorator, because it is passively triggered

- `app_autowired`:  
  
  - Function: Inject `app:App` arguments into the function instead of using `app:App= app_pool.get(session_util.get("app_id"))`  
  - Usage: As a decorator, be sure to follow the bot decorator, as this will cause the function to decrease one parameter
  
- `gen_control_keyboard`
  - Function: Generate control panel keyboard
  - Usage: Generate a `Keyboard` object
  - Parameters:
     - btn_data: buttons dict, see control panel text under `i18n`
     - btn_line: number of buttons per line, default two

- `gen_page_switch`
  - Function: Generate an up and down page switch button
  - Usage: Generate a list with up and down buttons, `Keyboard([gen_page_switch(...)])`
  - Parameters:
    - page_index: page number
    - has_next_page: is there a next page

### Attachment

#### Language code table
![lang.png](https://cdn.jsdelivr.net/gh/bitjerry/Microsoft-365-bot@main/img/lang.png)
