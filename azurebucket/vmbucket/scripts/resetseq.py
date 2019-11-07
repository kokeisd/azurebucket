import sqlite3

def deleteRecord():
    try:
        sqliteConnection = sqlite3.connect('../../db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")


        print("\n##### Check the sequnce before deleting #####")
        sql_select_query = 'select * FROM sqlite_sequence'
        #sql_delete_query = 'SELECT name from sqlite_master where type= "table"'
        cursor.execute(sql_select_query)
        print(cursor.fetchall())


        #print(cursor.fetchall())
        sql_delete_query = 'delete from sqlite_sequence where name="vmbucket_vmbucket"';
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        print("Record deleted successfully ")

        print("\n##### Check the sequnce after deleting #####")
        sql_select_query = 'select * FROM sqlite_sequence '
        cursor.execute(sql_select_query)
        print(cursor.fetchall())
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")

deleteRecord()
