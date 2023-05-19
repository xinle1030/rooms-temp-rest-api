import psycopg2
import os

url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)
ROOM_NAME = """SELECT name FROM rooms WHERE id = (%s)"""
ROOM_TERM = """SELECT DATE(temperatures.date) as reading_date,
AVG(temperatures.temperature)
FROM temperatures
WHERE temperatures.room_id = (%s)
GROUP BY reading_date
HAVING DATE(temperatures.date) > (SELECT MAX(DATE(temperatures.date))-(%s) FROM temperatures);"""

def get_room_term(room_id, term):
    terms = {"week": 7, "month": 30}
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ROOM_NAME, (room_id,))
            name = cursor.fetchone()[0]
            cursor.execute(ROOM_TERM, (room_id, terms[term]))
            dates_temperatures = cursor.fetchall()
    average = sum(day[1] for day in dates_temperatures) / len(dates_temperatures)
    return {
        "name": name,
        "temperatures": dates_temperatures,
        "average": round(average, 2),
    }