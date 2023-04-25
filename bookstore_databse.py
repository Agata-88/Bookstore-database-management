import sqlite3
db = sqlite3.connect('database/bookstore.db')
cursor = db.cursor() #get a cursor object

#create a table with headers (id,title,author and quantity)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookstore(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title TEXT,
        author TEXT,
        qty INTEGER)
''')
db.commit()

# Below deta will be added to the table
id1=3001
title1='A Tale of Two Cities'
author1='Charles Dickens'
qty1=30

id2=3002
title2='Harry Potter and the Philosopher\'s stone'
author2='J.K. Rowling'
qty2=40

id3=3003
title3='The Lion, the Witch and the Wardrobe'
author3='C.S. Lewis'
qty3=25

id4=3004
title4='The Lord of the Rings'
author4='J.R.R. Tolkien'
qty4=37

id5=3005
title5='Alice in Wonderland'
author5='Lewis Carroll'
qty5=30

id6=3006
title6='A Tale of Two Cities'
author6='Charles Dicken'
qty6=30

# Database is populated with above data, all 5 entries are added at one time.
books_data=[(id1,title1,author1,qty1), (id2,title2,author2,qty2),(id3,title3,author3,qty3),(id4,title4,author4,qty4),(id5,title5,author5,qty5),(id6,title6,author6,qty6)]
cursor.executemany('''INSERT or REPLACE INTO bookstore(id,title,author,qty) 
                    VALUES(?,?,?,?)''', (books_data))

print('books inserted')
db.commit()

#menu bookshop clerk will see.
print ("Welcome to bookstore database!\n")
while True:
    user_input = int(input("Please select one of the following options:\n"
        "1. Enter book\n"
        "2. Update book\n"
        "3. Delete book\n"
        "4. Search book\n"
        "5. Exit\n"))

    #adding new books
    if user_input == 1:
        title_input=input("Please enter new book title:")
        author_input=input("Please enter new book author:")
        qty_input=int(input("Please enter new book quantity:"))

        cursor.execute('''INSERT INTO bookstore(title,author,qty) 
                        VALUES(?,?,?)''',(title_input,author_input,qty_input))
        print(f'{title_input} by {author_input} has been added to the databse')
        db.commit()

    # Updating book information. Function checks if 'id' is in the table (list of ids) so it can be updated and if not
    # relevant information is displayed. 'Update' menu is displayed.
    id_data =[]
    if user_input==2:
        update_id_input=int(input("Please select id of the book you want to update:\n"))
        for data in books_data:
            id_data.append(data[0])
        if update_id_input not in id_data:
                print("Entered id cannot be found in the database, please try again")
                update_id_input=int(input("Please select id of the book you want to update:\n"))
        if update_id_input in id_data:
                update_detail_input=int(input("Please select one of the following options to update the file:\n"
                            "1. To update the title\n"
                            "2. To update the author\n"
                            "3. To update the quantity\n"
                            "4. To update all information\n"))
                            
        if update_detail_input == 1:
            update_title=input("Please confirm new title:\n")
            cursor.execute(('''UPDATE bookstore SET title=? WHERE id=?'''),(update_title,update_id_input))
            print(f'Title of book with id {update_id_input} has been changed to {update_title}')
            db.commit()
        
        if update_detail_input == 2:
            update_author=input("Please confirm new author:\n")
            cursor.execute(('''UPDATE bookstore SET author=? WHERE id=?'''),(update_author,update_id_input))
            print(f'Author of book with id {update_id_input} has been changed to {update_author}')
            db.commit()

        if update_detail_input == 3:
            update_qty=input("Please confirm new quantity for this book:\n")
            cursor.execute(('''UPDATE bookstore SET qty=? WHERE id=?'''),(update_qty,update_id_input))
            print(f'Quantity of book with id {update_id_input} has been changed to {update_qty}')
            db.commit()

        if update_detail_input == 4:
            update_title=input("Please confirm new title:\n")
            update_author=input("Please confirm new author:\n")
            update_qty=input("Please confirm new quantity for this book:\n")
            cursor.execute(('''UPDATE bookstore SET title=?,author=?,qty=? WHERE id=?'''),(update_title,update_author,update_qty,update_id_input))
            print(f'All details of book with id {update_id_input} have been changed to {update_title},{update_author},{update_qty}')
            db.commit()

    # Code to delete book from database
    if user_input==3:
            delete_id = input("Please confirm id of the book you would like to delete:\n")
            cursor.execute('''DELETE FROM bookstore WHERE id=?''',(delete_id,))
            print(f'Book {delete_id} has been removed from the databse')
            db.commit()

    # Below code allows user to seatch book by book id, title or author. 
    # If more than one the same title or author are found in the database
    # all are displayed.
    if user_input==4:
        search_book=int(input("Please enter one of the following options:\n"
                            "1. Search by book id\n"
                            "2. Search by title\n"
                            "3. Search by author\n"))
        if search_book==1:
            search_id = input("Please enter id of the book you are looking for:\n")
            cursor.execute('''SELECT * FROM bookstore WHERE id=?''',(search_id,))
            book = cursor.fetchone()
            print(f'Book you are looking for is {book[1]}, by {book[2]} and there are {book[3]} copies available.')
            db.commit

        if search_book==2:
            search_title = input("Please enter title of a book you are looking for:\n")
            cursor.execute('''SELECT * FROM bookstore WHERE title=?''',(search_title,))
            book = cursor.fetchall()
            print ("Books you are looking for are:")
            for titles in book:
                print (titles)

        if search_book==3:
            search_author = input("Please enter name of the author you are looking for:\n")
            cursor.execute('''SELECT * FROM bookstore WHERE author=?''',(search_author,))
            book = cursor.fetchall()    
            print ("Books by author you are looking for are:")
            for authors in book:
                print (authors)

    if user_input==5:
        print("Goodbye and see you soon!")
        break

db.commit()
db.close()
print('Connection to database closed')