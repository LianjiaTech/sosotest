# fake到没执行状态
【正式环境需要执行】
删除数据库表django_migrations里面的所有跟app 
all_models/all_models_for_dubbo/all_models_for_ui/all_models_for_mock/all_models_for_datacollect
相关的数据。

# 删除历史的migrations文件
到各个app目录下删除对应的那些migrations的文件
测试环境删除后，会重新migrate上传到正式环境，所以正式环境不需要执行此步骤。直接更新git即可。

# 重新生成初始化migrations文件
python3 manage.py makemigrations
测试环境会执行完然后上传到git，正式环境不需要执行此步骤。直接更新git即可。

# 将刚生成的migrations文件fake安装到数据库中
【正式环境需要执行】
python3 manage.py migrate --fake-initial

出现如下提示：
Operations to perform:
  Apply all migrations: admin, all_models, all_models_for_dubbo, all_models_for_mock, all_models_for_ui, auth, contenttypes, sessions
Running migrations:
  Applying all_models.0001_initial... FAKED
  Applying all_models_for_dubbo.0001_initial... FAKED
  Applying all_models_for_mock.0001_initial... FAKED
  Applying all_models_for_ui.0001_initial... FAKED

说明成功了。


