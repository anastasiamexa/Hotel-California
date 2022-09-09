import psycopg2

while True:
    print("Which query do you like to run?\n")
    print("(a)\n"
          "(b)\n"
          "(c)\n"
          "(d)\n"
          "(e)\n"
          "(f)\n"
          "(g)\n"
          "(h)\n"
          "exit\n")
    i = input("Choose a letter or type 'exit' if you want to terminate the program: ")
    if i == "a":
        sql_query = "SELECT COUNT(reservation_id),category FROM rooms INNER JOIN  reserved_rooms ON rooms.id = reserved_rooms.room_id GROUP BY category;"
        try:
            con = psycopg2.connect(dbname='Hotel California', host='localhost', port='5432', user='postgres',
                                   password='')
            cur = con.cursor()
            cur.execute(sql_query)
            records = cur.fetchall()
            for row in records:
                print("count: ", row[0])
                print("category: ", row[1])
            print("\n")
        except:
            print('error')
        finally:
            if (con):
                cur.close()
                con.close()
    elif i == "b":
        sql_query = '''WITH sum AS (SELECT SUM(transactions.total_cost) AS total_sum , category
                    FROM rooms INNER JOIN reserved_rooms ON rooms.id = reserved_rooms.room_id INNER JOIN transactions
                    ON reserved_rooms.reservation_id = transactions.reservation_id GROUP BY category)
                    SELECT *
                    FROM sum 
                    WHERE total_sum = (SELECT MAX(total_sum) FROM sum);'''
        try:
            con = psycopg2.connect(dbname='Hotel California', host='localhost', port='5432', user='postgres',
                                   password='')
            cur = con.cursor()
            cur.execute(sql_query)
            records = cur.fetchall()
            for row in records:
                print("total_sum:", row[0])
                print("category: ", row[1])
            print("\n")
        except:
            print('error')
        finally:
            if (con):
                cur.close()
                con.close()
    elif i == "c":
        sql_query = '''SELECT  COUNT(room_id) AS number_of_available_rooms
                    FROM    rooms INNER JOIN reserved_rooms ON rooms.id = reserved_rooms.room_id
                    INNER JOIN reservations ON reserved_rooms.reservation_id = reservations.id
                    WHERE NOT (date_in <= CURRENT_DATE AND date_out >= CURRENT_DATE);'''
        try:
            con = psycopg2.connect(dbname='Hotel California', host='localhost', port='5432', user='postgres',
                                   password='')
            cur = con.cursor()
            cur.execute(sql_query)
            records = cur.fetchall()
            for row in records:
                print("number of available rooms: ", row[0])
            print("\n")
        except:
            print('error')
        finally:
            if (con):
                cur.close()
                con.close()
    elif i == "d":
        sql_query = '''SELECT id, all_inclusive, breakfast, dinner, smoking, sea_view FROM ROOMS 
                    WHERE all_inclusive = 'true' OR breakfast= 'true' OR dinner = 'true' 
                    OR smoking = 'true' OR sea_view = 'true';'''
        try:
            con = psycopg2.connect(dbname='Hotel California', host='localhost', port='5432', user='postgres',
                                   password='')
            cur = con.cursor()
            cur.execute(sql_query)
            records = cur.fetchall()
            for row in records:
                print("id: ", row[0])
                print("all_inclusive: ", row[1])
                print("breakfast: ", row[2])
                print("dinner: ", row[3])
                print("smoking: ", row[4])
                print("sea view: ", row[5])
            print("\n")
        except:
            print('error')
        finally:
            if (con):
                cur.close()
                con.close()
    elif i == "e":
        sql_query = '''SELECT guests.id, fullname, date_in
                    FROM guests INNER JOIN transactions ON guests.customer_id = transactions.customer_id
                    INNER JOIN reservations ON transactions.reservation_id = reservations.id
                    WHERE date_part('month',date_in) = date_part('month',CURRENT_DATE) 
                    AND date_part('year',date_in) = date_part('year',CURRENT_DATE);'''
        try:
            con = psycopg2.connect(dbname='Hotel California', host='localhost', port='5432', user='postgres',
                                   password='')
            cur = con.cursor()
            cur.execute(sql_query)
            records = cur.fetchall()
            for row in records:
                print("id: ", row[0])
                print("full name: ", row[1])
                print("date in: ", row[2])
            print("\n")
        except:
            print('error')
        finally:
            if (con):
                cur.close()
                con.close()
    elif i == "f":
        sql_query = '''SELECT CAST(AVG(total_cost) AS DECIMAL(10,2)),rooms.category
                    FROM reservations INNER JOIN transactions ON reservations.id = transactions.reservation_id
                    INNER JOIN reserved_rooms ON transactions.reservation_id = reserved_rooms.reservation_id
                    INNER JOIN rooms ON rooms.id = reserved_rooms.reservation_id
                    WHERE date_part('month',date_in) = '06' OR
                    date_part('month',date_in) = '07' OR
                    date_part('month',date_in) = '08'
                    GROUP BY rooms.category;'''
        try:
            con = psycopg2.connect(dbname='Hotel California', host='localhost', port='5432', user='postgres',
                                   password='')
            cur = con.cursor()
            cur.execute(sql_query)
            records = cur.fetchall()
            for row in records:
                print("average: ", row[0])
                print("category: ", row[1])
            print("\n")
        except:
            print('error')
        finally:
            if (con):
                cur.close()
                con.close()
    elif i == "g":
        sql_query = '''(WITH max AS (SELECT customer_id, COUNT(financial_zone) AS max_reservations,financial_zone
                            FROM rooms INNER JOIN reserved_rooms ON rooms.id = reserved_rooms.room_id
                            INNER JOIN transactions ON transactions.reservation_id = reserved_rooms.reservation_id
                            WHERE financial_zone = 'low'
                            GROUP BY customer_id,financial_zone)
                            SELECT customer_id, max_reservations,financial_zone
                            FROM max
                            WHERE max_reservations = (SELECT MAX(max_reservations) FROM max))
                            UNION
                            (WITH max AS (SELECT customer_id, COUNT(financial_zone) AS max_reservations,financial_zone
                            FROM rooms INNER JOIN reserved_rooms ON rooms.id = reserved_rooms.room_id
                            INNER JOIN transactions ON transactions.reservation_id = reserved_rooms.reservation_id
                            WHERE financial_zone = 'medium'
                            GROUP BY customer_id,financial_zone)
                            SELECT customer_id, max_reservations,financial_zone
                            FROM max
                            WHERE max_reservations = (SELECT MAX(max_reservations) FROM max))
                            UNION
                            (WITH max AS (SELECT customer_id, COUNT(financial_zone) AS max_reservations,financial_zone
                            FROM rooms INNER JOIN reserved_rooms ON rooms.id = reserved_rooms.room_id
                            INNER JOIN transactions ON transactions.reservation_id = reserved_rooms.reservation_id
                            WHERE financial_zone = 'high'
                            GROUP BY customer_id,financial_zone)
                            SELECT customer_id, max_reservations,financial_zone
                            FROM max
                            WHERE max_reservations = (SELECT MAX(max_reservations) FROM max));'''

        try:
            con = psycopg2.connect(dbname='Hotel California', host='localhost', port='5432', user='postgres',
                                   password='')
            cur = con.cursor()
            cur.execute(sql_query)
            records = cur.fetchall()
            for row in records:
                print("customer id: ", row[0])
                print("max reservations: ", row[1])
                print("financial zone: ", row[2])
            print("\n")
        except:
            print('error')
        finally:
            if (con):
                cur.close()
                con.close()
    elif i == "h":
        sql_query = '''SELECT room_id , date_in, date_out
                    FROM reserved_rooms INNER JOIN reservations ON reserved_rooms.reservation_id = reservations.id
                    WHERE date_in <= CURRENT_DATE AND date_in >= '2017-06-28' ORDER BY room_id;'''
        try:
            con = psycopg2.connect(dbname='Hotel California', host='localhost', port='5432', user='postgres',
                                   password='')
            cur = con.cursor()
            cur.execute(sql_query)
            records = cur.fetchall()
            for row in records:
                print("room id: ", row[0])
                print("date in: ", row[1])
                print("date out: ", row[2])
            print("\n")
        except:
            print('error')
        finally:
            if (con):
                cur.close()
                con.close()
    elif i == "exit":
        break
    else:
        print("Wrong input!")