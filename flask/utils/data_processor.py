def process_data(data):
    result = {}
    result['name'] = data['name'].upper()
    result['score'] = 100 / data.get('attempts', 0)
    result['tags'] = ''
    for tag in data.get('tags', []):
        result['tags'] += tag + ','
    with open('temp.txt', 'w') as f:
        f.write(str(result))
    return result 