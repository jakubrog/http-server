

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
        self.result += '<h' + str(number) + '>' + str(text) + '</h' + str(number) + '>'

    def get_HTML(self):
        return self.result + "</body>\n</html>"

    # dict must contains {name : value}
    def add_select_from_list(self, query_name, action, dic):
        self.result += '<form action=\"/' + action + '\" method=\"GET\">\n'
        self.result += "<select name=" + query_name + " id=" + action + "</select>\n"
        self.result += '\t<option value="">--Please choose an option--</option>\n'
        for key in dic.keys():
            self.result += '\t<option value=' + dic[key] + ">" + key + "</option>\n"
        self.result += '</select>\n<input type="submit" value="Submit"/>\n'
        self.result += '</form>'

    # dic - keys; text to be displayed, values; uri 
    def add_clickable_list(self, dic):
        self.result += '\n<ul>\n'
        for key in dic.keys():
            self.result += '\t<li>'
            self.result += "<a href=\"" + dic[key] +'\">' + key + '</a></li>\n'
        self.result += '</ul>\n'