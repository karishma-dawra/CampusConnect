import sqlite3

def init_db():
    #Connects to 'campusconnect.db'
    conn=sqlite3.connect("campusconnect.db") #created connector object
    cursor=conn.cursor() #created a cursor

    cursor.execute(
        """
        CREATE TABLE if not exists users(
        ID integer primary key,
        NAME text not null,
        Email text unique not null,
        Password text not null
        )
        """
    )
    conn.commit()
    conn.close()
    print("database created successfully")

if __name__ == "__main__":
    init_db()