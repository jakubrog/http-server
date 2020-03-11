

class Generator():
    def __init__(self, title):
        
        with open('base.html', 'rb') as file: 
            self.result = file.read().decode()
        self.result +=  '\t<title>' + title + '</title>\n</head>\n<body>'
        
    def add_list(self, list):
        self.result += '\n<ul>\n'
        for element in list:
            self.result += '\t<li>' + str(element) + '</li>\n'
        self.result += '</ul>\n'

    def add_header(self, text, number=1):
        self.result += '<h' + str(number) + '>' + text + '</h' + str(number) + '>'

    def get_HTML(self):
        return self.result + "</body>\n</html>"

    # dict must contains {name : value}
    def add_select_from_list(self, query_name, action, dict):
        self.result += '<form action=\"/' + action + '\" method=\"GET\">\n'
        self.result += "<select name=" + query_name + " id=" + action + "</select>\n"
        self.result += '\t<option value="">--Please choose an option--</option>\n'
        for key in dict.keys():
            self.result += '\t<option value=' + dict[key] + ">" + key + "</option>\n"
        self.result += '</select>\n<input type="submit" value="Submit"/>\n'
        self.result += '</form>'
