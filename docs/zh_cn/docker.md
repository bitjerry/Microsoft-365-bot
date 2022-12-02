### 部署

> 你可以看到在Dockerfile中写了一些环境变量, 这与配置选项是相同的  
> 当然你也可以不写, 比如你原来系统就设置有相应的环境变量  

1. fly.io  
把`fly.toml`的`[build]`切换就可以了

2. heroku  
请去它们的官网查看, 它们有直接的一套发布docker的命令行

3. VPS
    ```commandline
    docker build -t xxx
    ```