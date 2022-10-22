# Q&A

### Error with ORM

When you use a different database, there may be a running error. 
The default driver for some databases is included in orm, 
but there may still be an error that xxx cannot be found. 
At this point, please install the required database driver package manually, 
`pip install xxx` or write the package to `requirements.txt`

### Command not responding

If it is an individual case, please go to the readme document to check the command list. After the project is updated, new commands may be added. Generally, existing commands will not be modified unless a major version is updated.   

If most of them are unresponsive, please use `/log` to view the robot log.

### InvalidAuthenticationToken

When switching to a new app, an immediate request may appear
> {'error': {'code': 'InvalidAuthenticationToken', 'message': 'CompactToken parsing failed with error code: 80049217', 'innerError': {'date': '2022-09-26T15:00:36', 'request-id': '2e1dfda1-63f2-4c23-a584-df45cb282b03', 'client-request-id': '2e1dfda1-63f2-4c23-a584-df45cb282b03'}}}

This problem should belong to Microsoft's API. It is known that if the same app has already requested a token, requesting a new token will not take effect immediately. It only takes a while. The program will redeem the token after loading the app, and refresh it after expiration. Considering that the user may have the most app, it is impossible to load all apps into the app pool at one time, so the token is lazy to load.

### Insufficient privileges to complete the operation

1. First check if the API permissions are sufficient
2. If Microsoft Global accounts are restricted, some features may not be available. Please submit ticket to Microsoft to solve the problem.
3. Changing user passwords requires special permissions, see [here](https://stackoverflow.com/questions/61004464/how-to-update-the-password-of-user-in-azure-ad-using-graph-api).

### Why is it taking so long to get data

First of all, this is not a problem of python,~~nor is it a problem of my code quality (joke)~~ Such a small project can't reach the bottleneck of python, such a delay is almost impossible for users to feel, mainly caused by two aspects. Significant delay:
1. Microsoft API responses, accounting for 80% of latency
2. Telegram server delay

### Why is robot UI so ugly

Mainly due to the following two reasons:
1. Due to the limitation of telegram's message format, the styles supported by messages are whether html or markdown.
All are very limited, the robot can send the keyboard, add up to a few emoji, that's all.
2. Let me know if you have any good ideas.

### Other questions

- Startup failure: Check the machine terminal, the error message will be output directly
- Runtime error: Use `/log` to get the robot run log
- Bug: Feedback issues, or set environment variables `DEBUG=True`
- Others: Feedback issues.
