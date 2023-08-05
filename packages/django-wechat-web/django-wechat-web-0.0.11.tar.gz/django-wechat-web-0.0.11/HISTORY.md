# django-wechat-web 

### 2016-04-29
* Fix Bug
    * 问题: 第一次授权的时候就去哪用户信息导致奔溃
    * 解决: 设置一个是否存储用户信息的变量save_userinfo_or_not, 默认为False, 只有满足需要获取userinfo的条件时才设为True, 然后才获取用户信息
* Fix Bug
    * error function args
* update WechatView
    * scope设置为snsapi_userinfo 时，说明希望保留用户详细信息
    * 但是, 又不希望用户多次snsapi_userinfo方式授权, 所以过程是这样的

```
    -> 1.默认snsapi_base方式跳转 
    -> 2.拿到code, 获取openid, 将openid存到session 
    -> 3.如果openid存在并且openid对应的WechatUserInfo模型数据不存在并且scope为snsapi_userinfo, 则将再次跳转到snsapi_userinfo方式; 如果openid不存在, 或者openid存在，但WechatUserInfo数据存在, 或者 openid存在，但是scope不是snsapi_userinfo, 则跳转第五步
    -> 4.跳回步骤2
    -> 5. 授权结束, 接下来执行你的动作
```

### 2016-04-27
* update WechatView
  * add class boolean attr: swicth
    * `swicth=True` (default): open wechat redirect/authentication
    * `swicth=False` : The same as django.views.generic.View

