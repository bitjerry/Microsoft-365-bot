### Deploy

> You can see that some environment variables are written in Dockerfile, which is the same as the configuration options  
> Of course, you can not write it. For example, your system has set corresponding environment variables 

1. fly.io  
Just change the value `fly.toml`->`[build]`

2. heroku  
See heroku website. They have a set of command lines to release dockers

3. VPS
    ```commandline
    docker build -t xxx
    ```