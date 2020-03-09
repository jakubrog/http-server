# returns dictionary of names and values of given queries
# ex. name=Jan&surname=Kowalski => {'name': 'Jan', 'surname': 'kowalski' }
def parse_query(query):
    queries = query.split('&')
    result = {}
    for q in queries:
        q = q.split('=')
        if len(q) == 2:
            result[q[0]] = q[1]
    return result
