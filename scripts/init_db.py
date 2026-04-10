import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import create_app
from backend.database import add_log


def main():
    # 初始化数据库并写入启动日志
    create_app()
    add_log("脚本执行", "已通过 scripts/init_db.py 完成数据库初始化")
    print("数据库初始化完成")


if __name__ == "__main__":
    main()
