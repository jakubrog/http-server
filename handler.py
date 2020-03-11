from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from http.server import HTTPServer
from query_parser import parse_query
import football
import html_generator

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.handle_main()
        elif parsed_path.path == '/teams':
            self.handle_team_request(parsed_path.query)
        elif parsed_path.path == '/competitions':
            self.handle_competition_request(parsed_path.query)
        elif parsed_path.path == '/players':
            self.handle_player_request(parsed_path.query)
        else:
            self.handle_not_found()

    # handling path "/"
    def handle_main(self):
        self.send_response(200)
        self.end_headers()
        x = football.get_club_selection("id", "teams")
        self.wfile.write(x.encode())
    
    # handle path /teams and /teams?{id}
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
            x = football.get_club_list()
            self.wfile.write(x.encode())
        else:
            self.handle_not_found()

    # handle path /competition?{id} or name
    def handle_competition_request(self, query):
        query = parse_query(query)
        if 'id' in query.keys():
            id = query['id']
            self.send_response(200)
            self.end_headers() 
            # x = football.get_club_list()
            self.wfile.write(("Looking for competition " + id).encode())
        else:
            self.handle_not_found()

    # handle path /player=?{id} or name
    def handle_player_request(self, query):
        query = parse_query(query)
        if 'id' in query.keys():
            id = query['id']
            self.send_response(200)
            self.end_headers() 
            x = football.get_player_info(id)
            self.wfile.write(x.encode())
        else:
            self.handle_not_found()
    
    def handle_not_found(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write("<h1>Page not found</h1>".encode())

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), ServerHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()