import http.server
import os
import socketserver


def main():
    # 使用 Python 内置静态服务启动前端页面，避免额外依赖
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(project_root, "frontend")
    os.chdir(frontend_dir)
    port = 5500
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"前端服务启动成功: http://127.0.0.1:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
