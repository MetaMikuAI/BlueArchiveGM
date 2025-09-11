from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import requests
import json

BACKEND_API = "http://localhost:5000"
SHOW_ALL_RESPONSES = True


class ProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # 拦截 OPTIONS 请求并欺骗允许所有方法
        self.handle_options()
    
    def do_GET(self):
        self.forward_request('GET')
    
    def do_POST(self):
        self.forward_request('POST')
    
    def do_PUT(self):
        self.forward_request('PUT')
    
    def do_DELETE(self):
        self.forward_request('DELETE')
    
    def handle_options(self):
        # 构建允许所有方法的响应
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        # 动态返回前端请求的 Access-Control-Request-Headers
        req_headers = self.headers.get('Access-Control-Request-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Headers', req_headers)
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()



    def forward_request(self, method):
        target_url = BACKEND_API + self.path

        hop_by_hop = [
            'host', 'content-length', 'accept-encoding', 'connection',
            'keep-alive', 'proxy-authenticate', 'proxy-authorization',
            'te', 'trailers', 'transfer-encoding', 'upgrade'
        ]
        headers = {key: value for key, value in self.headers.items() if key.lower() not in hop_by_hop}

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None
        try:
            response = requests.request(
                method=method,
                url=target_url,
                headers=headers,
                data=body,
                timeout=30
            )
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                if key.lower() not in ['transfer-encoding', 'connection', 'content-encoding']:
                    self.send_header(key, value)
            
            self.send_header('Access-Control-Allow-Origin', '*') # IMPORTANT for CORS
            self.end_headers()

            if SHOW_ALL_RESPONSES:
                print(response.content)
            
            self.wfile.write(response.content)
            self.wfile.flush()
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_msg = json.dumps({'error': str(e)})
            self.wfile.write(error_msg.encode('utf-8'))

def run_proxy(server_class=HTTPServer, handler_class=ProxyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting proxy server on port {port}...')
    print(f'Proxy will convert all OPTIONS requests to GET and forward to backend')
    httpd.serve_forever()

if __name__ == '__main__':
    run_proxy(port=8080)