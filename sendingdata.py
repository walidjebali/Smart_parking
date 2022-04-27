from count import *
import pyrebase


firebaseConfig = {
     'apiKey': "TXp6PAw54VCdgLomVzEgmvyczT7BE9wg0S5k0pcn",
    'authDomain': "Parkinny-test.firebaseapp.com",
    'databaseURL': "https://parkinny-test-default-rtdb.firebaseio.com/",
    'storageBucket': "Parkinny-test.appspot.com",
    }
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
max_pixel = 900

while True:
    with open("count.py", "r") as r:
        lines = r.readlines()
        for i in range(len(lines)):
            print('test')

            if float(lines[i]) < max_pixel:
                db.child(i).set('0  ')
            elif float(lines[i]) > max_pixel:
                db.child(i).set('1  ')
            db.child(i - 10).remove()
