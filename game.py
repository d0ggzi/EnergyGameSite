from flask import Flask, render_template

app = Flask(__name__)

lines = [
    [{'name': 'Больница', 'potreb': 10, 'next_potreb': 15},
    {'name': 'Завод', 'potreb': 15, 'next_potreb': 20}],
    [{'name': 'Жилой дом', 'potreb': 5, 'next_potreb': 13},
    {'name': 'Жилой дом', 'potreb': 8, 'next_potreb': 18},
    {'name': 'Жилой дом', 'potreb': 15, 'next_potreb': 23},
    {'name': 'Жилой дом', 'potreb': 15, 'next_potreb': 23},
    {'name': 'Жилой дом', 'potreb': 15, 'next_potreb': 23}],
    [{'name': 'Ларек', 'potreb': 2, 'next_potreb': 2},
    {'name': 'Шавуха', 'potreb': 3, 'next_potreb': 3}]
]

def ab():
    print('sosi')

@app.route('/')
def index():
    ab()
    return render_template('index.html', lines=lines)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)