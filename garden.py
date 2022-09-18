#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error
from adafruit_seesaw.seesaw import Seesaw
import time
import board


def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
        print("DB connection success")
    except Error as err:
            print(f"Error: '{err}'")

    return connection


def insertRecord(connection, data):
    cursor = connection.cursor()

    add_soil = ("INSERT INTO soil "
                "(moisture, temperature, date_stamp, epoch)"
                "VALUES (%s, %s, %s, %s)")
    cursor.execute(add_soil, data)
    connection.commit()
    cursor.close()




#our humidity/temperaturer sensor
i2c_bus = board.I2C()
ss = Seesaw(i2c_bus, addr=0x36)


pw = "super_secret_pw"

#attempt tp create DB connection
connection = create_server_connection("localhost", "sensor", pw, "garden")



try: 
    while True:

        #get our timestamps()
        localtime = time.localtime()
        time_stamp = time.strftime("%d:%m:%Y %I:%M:%S %p", localtime)
        epoch = int(time.time())


        #get our sensor readings
        touch = ss.moisture_read()
        temp = ss.get_temp()


        #insert our record into the DB and wait
        insertRecord(connection, (touch, temp, time_stamp, epoch))
        time.sleep(30)
        

       # print(f"temp: {round(temp, 2)}c ----------- moisture: {touch}")

finally:
    connection.close();
    print('done')
