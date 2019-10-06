
### 该项目已停止更新，新进开发转移至https://github.com/mahaoxiang822/VisualPytorch
### 如有疑问请email 464365439@qq.com

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

