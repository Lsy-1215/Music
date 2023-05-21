SECRET_KEY = "01234567899876543210"


# 数据库配置信息
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'demo01'
USERNAME = 'root'
PASSWORD = 'Li456258'
DB_URI   = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "2270498357@qq.com"
MAIL_PASSWORD = "rvedzvgdzqbndjbc"
MAIL_DEFAULT_SENDER = "2270498357@qq.com"
# 授权码：rvedzvgdzqbndjbc

