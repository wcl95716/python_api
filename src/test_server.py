from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
import threading
import time
import socket

class MultiPortServer:
    def __init__(self, start_port, end_port):
        self.start_port = start_port
        self.end_port = end_port
        self.servers = []
        self.threads = []
        self.failed_ports = []

    def run_server(self, port):
        try:
            server_address = ('', port)
            httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
            print(f"服务器运行在端口 {port}")
            self.servers.append(httpd)
            httpd.serve_forever()
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"端口 {port} 已被占用")
                self.failed_ports.append(port)
            else:
                print(f"端口 {port} 启动失败: {str(e)}")
                self.failed_ports.append(port)

    def start(self):
        for port in range(self.start_port, self.end_port + 1):
            thread = threading.Thread(target=self.run_server, args=(port,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
            print(f"尝试启动端口 {port} 的服务器")
            time.sleep(0.1)  # 避免端口冲突

    def stop(self):
        for server in self.servers:
            server.shutdown()
        for thread in self.threads:
            thread.join()

def main():
    if len(sys.argv) != 3:
        print("使用方法: python test_server.py <起始端口> <结束端口>")
        sys.exit(1)
    
    start_port = int(sys.argv[1])
    end_port = int(sys.argv[2])
    
    server = MultiPortServer(start_port, end_port)
    try:
        server.start()
        print(f"\n服务器启动完成:")
        print(f"- 成功启动的端口: {[port for port in range(start_port, end_port + 1) if port not in server.failed_ports]}")
        if server.failed_ports:
            print(f"- 启动失败的端口: {server.failed_ports}")
        print("\n按 Ctrl+C 停止所有服务器")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止所有服务器...")
        server.stop()
        print("所有服务器已停止")

if __name__ == '__main__':
    main() 