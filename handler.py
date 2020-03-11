from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from http.server import HTTPServer
from query_parser import parse_query
import football
import html_generator

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.handle_main()
        elif parsed_path.path == '/teams':
            self.handle_team_request(parsed_path.query)

    # handling path "/"
    def handle_main(self):
        self.send_response(200)
        self.end_headers()
        x = football.get_club_selection("id", "teams")
        self.wfile.write(x.encode())
    
    # handle path /teams and /teams?={id}
    def handle_team_request(self, query):
        query = parse_query(query)
        if 'id' in query.keys():
            team_id = query['id']
            self.send_response(200)
            self.end_headers() 
            result = football.get_club_info(team_id)
            self.wfile.write(result.encode())
        elif not query:
            self.send_response(200)
            self.end_headers() 
            self.wfile.write(football.get_club_list().encode())
        
    
if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()