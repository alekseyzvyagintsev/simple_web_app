from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    css_path = "/css/bootstrap.min.css"

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Выполняем проверку запроса пользователя '/'
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif parsed_path.path.startswith('/css'):
            try:
                with open(f'.{parsed_path.path}', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/css')
                    self.end_headers()
                    self.wfile.write(file.read())
                    return
            except FileNotFoundError:
                self.send_error(404, "CSS File Not Found")
                return
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('contacts.html', 'rb') as file:
                self.wfile.write(file.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Печатаем полученные данные в консоли
        print(f"Полученные данные из POST запроса:\n{post_data}")

        # Ответ клиенту (например, подтверждение успешного принятия данных)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Data received successfully!')


def run():
    web_server = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    run()