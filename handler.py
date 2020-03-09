from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from http.server import HTTPServer
from query_parser import parse_query
class GetHandler(BaseHTTPRequestHandler):

    # def do_GET(self):
    #     parsed_path = urlparse(self.path)

    #     message_parts = [
    #             'CLIENT VALUES:',
    #             'client_address=%s (%s)' % (self.client_address,
    #                                         self.address_string()),

    #             'path=%s' % self.path,
    #             'real path=%s' % parsed_path.path,
    #             'query=%s' % parsed_path.query,
    #             'request_version=%s' % self.request_version,
    #             '',
    #             'SERVER VALUES:',
    #             'server_version=%s' % self.server_version,
    #             'sys_version=%s' % self.sys_version,
    #             'protocol_version=%s' % self.protocol_version,
    #             '',
    #             'HEADERS RECEIVED:',
    #             ]
    #     for name, value in sorted(self.headers.items()):
    #         message_parts.append('%s=%s' % (name, value.rstrip()))
    #     message_parts.append('')
    #     message = '\r\n'.join(message_parts)
    #     self.send_response(200)
    #     self.end_headers()
    #     self.wfile.write(message.encode())
    #     return

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self._handle_main()
        elif parsed_path.path == '/teams':
            self.handle_team_request(parsed_path.query)

    # handling path "/"
    def _handle_main(self):
        self.send_response(200)
        self.end_headers()
        with open('index.html', 'rb') as file: 
            self.wfile.write(file.read())

    def handle_team_request(self, query):
        query = parse_query(query)
        if 'name' in query.keys():
            team_name = query['name']
            self.send_response(200)
            self.end_headers() 
            self.wfile.write(("<h1>HEY THERE!!! Looking for: " +  team_name + "</h1>").encode())
            return
        elif not query:
            self.send_response(200)
            self.end_headers() 
            self.wfile.write(("<h1>HEY THERE!!! Wanna know what teams you have</h1>").encode())

        
    
if __name__ == '__main__':
    
    server = HTTPServer(('localhost', 8080), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()