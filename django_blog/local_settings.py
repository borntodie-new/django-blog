from .settings import INSTALLED_APPS, BASE_DIR

# 注册APP
apps = [
    # 注册后台APP
    'backend.apps.BackendConfig',
]
INSTALLED_APPS.extend(apps)

# 项目本地化
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = False

# 配置静态文件夹地址
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
