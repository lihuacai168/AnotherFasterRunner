import pymysql

# 替换mysqlclient
pymysql.version_info = (1, 4, 6, "final", 0)  # 修改版本号为兼容版本
pymysql.install_as_MySQLdb()

