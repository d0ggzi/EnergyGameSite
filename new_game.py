# coding=utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from flask import Flask, render_template
# import serial
from random import randint as rnd
import time, json

app = Flask(__name__)

lines = [
    [{'name': 'Больница', 'potreb': 10, 'next_potreb': 15},
     {'name': 'Завод', 'potreb': 15, 'next_potreb': 20}],
    [{'name': 'Завод', 'potreb': 5, 'next_potreb': 13},
     {'name': 'Жилой дом', 'potreb': 8, 'next_potreb': 18},
     {'name': 'Жилой дом', 'potreb': 15, 'next_potreb': 23}],
    [{'name': 'Жилой дом', 'potreb': 2, 'next_potreb': 2},
     {'name': 'Жилой дом', 'potreb': 3, 'next_potreb': 3}]
]


def turning(zapas, data):
    print('before ', data, zapas)
    for i in range(len(lines)):
        if data[i]:
            zapas2 = zapas
            for house in lines[i]:
                if zapas - house['potreb'] < 0:
                    data[i] = 0
                    zapas = zapas2
                    break
                else:
                    zapas -= house['potreb']
    print('after ', data, zapas)
    return zapas, data


def potrebl(data):
    print('before ', lines)
    for i in range(len(lines)):
        for house in lines[i]:
            house['potreb'] = int(house['next_potreb'] * int(data[i]) * rnd(90, 110) / 100)
    print('after ', lines)


def schet(score, data):
    for i in range(len(lines)):
        for house in lines[i]:
            if house['name'] == 'Больница':
                if data[i] == 0:
                    score -= 100
                else:
                    score += 15
            elif house['name'] == 'Завод':
                if data[i] == 0:
                    score -= 50
                else:
                    score += 25
            else:
                if data[i] == 0:
                    score -= 15
                else:
                    score += 10

    return score


def prediction(t, kfpt):
    if t == 5: t = 1
    for line in lines:
        for house in line:
            if house['name'] == 'Больница':
                if t == 1:
                    house['next_potreb'] = rnd(15, 25)
                else:
                    house['next_potreb'] = rnd(10, 20)
            elif house['name'] == 'Завод':
                if t == 1:
                    house['next_potreb'] = rnd(10, 20)
                elif t == 2:
                    house['next_potreb'] = rnd(30, 45)
                elif t == 3:
                    house['next_potreb'] = rnd(15, 25)
                else:
                    house['next_potreb'] = 0
            else:
                if t == 1:
                    house['next_potreb'] = rnd(8, 13)
                elif t == 2:
                    house['next_potreb'] = rnd(5, 12)
                elif t == 3:
                    house['next_potreb'] = rnd(18, 30)
                else:
                    house['next_potreb'] = rnd(2, 5)
            house['next_potreb'] = int(house['next_potreb'] * kfpt)


def sendToLed(bright, ser):
    for i in range(2):
        for i in range(5):
            ser.write(str(bright[i]).encode())
            time.sleep(0.3)
        ser.write('!'.encode())
        print("Sending data...")


@app.route('/')
@app.route('/index')
@app.route('/index/<int:NumRound>')
def index(NumRound=0):
    global data, day_time, h_balloon, zapas, score
    kfpt = 0.9
    if NumRound == 0:
        day_time, zapas, score, solar_prod, fuel_prod, h_balloon = 1, 120, 100, 0, 0, 5
        data = [0] * len(lines) + [0]
    else:
        day_time += 1
        if day_time == 5:
            day_time = 1
        h_balloon -= data[-1]
        solar_prod = round(rnd(12, 20) / 10 * 12, 1)
        fuel_prod = round(rnd(12, 15) / 10 * 12, 1) * data[-1]
        zapas = round(zapas + solar_prod + fuel_prod, 1)
        potreb = potrebl(data)
        zapas, data = turning(zapas, data)
        score = schet(score, data)
        # SendToLed(bright,ser)
    prediction(day_time + 1, kfpt)
    print(NumRound, data)
    day_time_str = ['-', 'Утро', 'День', 'Вечер', 'Ночь'][day_time]
    return render_template('index.html', lines=lines, score=score, zapas=zapas, day_time=day_time_str, h_balloon=h_balloon, solar_prod=solar_prod, fuel_prod=fuel_prod, data=data)


@app.route('/get/<data1>', methods=["POST", "GET"])
def get(data1):
    global data
    data = json.loads(data1)['city']

    return 'Info received with no problems.'


if __name__ == '__main__':
    # ser = serial.Serial("/dev/ttyACM0", 9600)
    app.run(host='0.0.0.0', port='80', debug=True)
