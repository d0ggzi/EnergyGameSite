lines = [
    [{'name': 'hosp', 'potreb': 12},
     {'name': 'zavod', 'potreb': 15}],
    [{'name': 'house', 'potreb': 13},
     {'name': 'house', 'potreb': 18}]
]

def izmena():
    for line in lines:
        for house in line:
            house['potreb'] = 3


izmena()
print(lines)