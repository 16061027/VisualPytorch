# VisualPytorch

### 一、测试环境配置说明

1、拉取develop分支后

```
pip install -r requirements.txt
```

2、进入VisualPytorch/config/config.py下配置数据库设置

3、启动后台服务器

```
python manage.py runserver 8000
```

4、可能需要向数据库中迁移模型

```
python manage.py migrate
```

