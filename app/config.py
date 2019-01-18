# Created by carryon on 19-1-14.
import os

# 获取到config所在的目录 定义基础目录
base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    # 密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jiangxiligong'
    # 数据库的操作
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = '127.0.0.1'
    PORT = '3306'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or 'smtp.qq.com'
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or 'carryonzll@qq.com'
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or 'iygataacwnjyffcj'
    # bootstrap 使用本地静态文件
    BOOTSTRAP_SERVE_LOCAL = True
    BOOTSTRAP_QUERYSTRING_REVVING = True
    # 上传文件 配置
    MAX_CONTENT_LENTH = 1024 * 1024 * 8
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload/')

    @staticmethod  # 静态方法 类才可以调用
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    DATABASE = 'py_study'
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(Config.DIALECT, Config.DRIVER,
                                                                           Config.USERNAME, Config.PASSWORD,
                                                                           Config.HOST, Config.PORT, DATABASE)


# 测试环境配置
class TestingConfig(Config):
    DATABASE = 'test'
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(Config.DIALECT, Config.DRIVER,
                                                                           Config.USERNAME, Config.PASSWORD,
                                                                           Config.HOST, Config.PORT, DATABASE)


# 生产环境配置
class ProductionConfig(Config):
    DATABASE = 'practice'
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(Config.DIALECT, Config.DRIVER,
                                                                           Config.USERNAME, Config.PASSWORD,
                                                                           Config.HOST, Config.PORT, DATABASE)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
