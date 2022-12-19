#!/usr/bin/python3
import socket, os, sys, threading, argparse, hashlib, mysql.connector, time, multiprocessing
from multiprocessing import Process

#logging.basicConfig(filename='readerlist_app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

while True:
    #Connect to MySQL database
    try:
        conn = mysql.connector.connect(host='127.0.0.1', user='readlyst', password='P@ssw0rd', database='readlyst')
        print("[+] Successfully connected to MySQL database [+]")
        # logging.info('Connected to DB')
    except mysql.connector.Error as error:
        print(f"[-] Failed to connect to MySQL database: {error} [-]")
        # logging.error('Failed connect to DB')
        # logging.error('%s raised an error', conn)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, help="Port number to listen on")
    args = parser.parse_args()
    port = args.p

    #Set up socket to listen on port 9090
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen()

    def handle_client(client, addr):
        client.send(b"\n                    ,---------------------------,")
        client.send(b"\n                    |  /---------------------   |")
        client.send(b"\n                    | |                       | |")
        client.send(b"\n                    | |       Readmark        | |")
        client.send(b"\n                    | |      iHACK 2022       | |")
        client.send(b"\n                    | |       @x786683        | |")
        client.send(b"\n                    | |                       | |")
        client.send(b"\n                    |  _____________________ /  |")
        client.send(b"\n                    |___________________________|")
        client.send(b"\n              ,---_____     []     _______/------,")
        client.send(b"\n             /         /______________           /|")
        client.send(b"\n            /___________________________________ /  | ___")
        client.send(b"\n            |                                   |   |    )")
        client.send(b"\n            |  _ _ _                 [-------]  |   |   (")
        client.send(b"\n            |  o o o                 [-------]  |  /    _)_")
        client.send(b"\n            |__________________________________ |/     /  /")
        client.send(b"\n            /-------------------------------------/|  ( )/")
        client.send(b"\n           /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /")
        client.send(b"\n          /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /")
        client.send(b"\n          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        client.send(b"\n######################################################################")
        client.send(b"\n###                Welcome To Readmark Service :)                  ###\n")
        client.send(b"######################################################################\n")

        client.send(b"\n### Please enter your email and password; eg admin@readlyst.io:password01 ###\n")

        while True:
            try:

                email, password = client.recv(1024).decode().split(":")
                password_hash = hashlib.sha1(password.rstrip().encode('utf-8')).hexdigest()

                cursor = conn.cursor()
                result = cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password_hash))
                result = cursor.fetchone()
                # check if the email and password are correct
                if result:
                    # if they are correct, proceed to the next option

                    client.send(b"\n[+]  Login successful!\n")
                    time.sleep(3)

                    # Search for email in MySQL database
                    cursor = conn.cursor()
                    query = "SELECT username FROM users WHERE email=%s"
                    cursor.execute(query, (email,))
                    username = cursor.fetchone()
                    if type(username) == tuple:
                        username = username[0]
                    else:
                        client.send(b"\n[-]  The is no current email in the Readlyst system. Please exit & restart!!\n")

                    # Check if email exists in database
                    # Email exists, evaluate the email
                    if username:
                        try:
                            client.send(result = eval(username))
                        except Exception as error:
                            pass
                            #logging.error(error)

                        username = str(username).encode('utf-8')
                        client.send(b"\n[+]  Welcome : " + username + b"\n")
                        
                    else:
                        client.send(b"[-]  Do recheck the email in Readlyst system\n")
                        exit()

                    #client.send(b"\n######################################")
                    client.send(b"\n### Searching user_id for " + username + b"\n")
                    #client.send(b"######################################\n")
                    # Search for email in MySQL database
                    time.sleep(2)
                    cursor = conn.cursor()
                    query_uid = "SELECT user_id FROM users WHERE email=%s"
                    cursor.execute(query_uid, (email,))
                    uid = cursor.fetchone()[0]
                    b_uid = str(uid).encode('utf-8')
                    client.send(b"\n[+]  The USER_ID is: " + b_uid + b"\n")

                    cursor = conn.cursor()
                    query_book = "SELECT list_id,title from books join read_list on books.book_id = read_list.book_id where read_list.user_id = %s"
                    cursor.execute(query_book, (uid,))
                    book_id = cursor.fetchall()

                    # Print each book_id value in a separate row
                    client.send(b"\n### Searching for books in reading list for " + username + b"\n")
                    time.sleep(2)
                    if len(book_id) == 0:
                        client.send(b"\n[-]  No reading list. Please add some books to reading list ;)\n[-]  Exiting!!")
                        exit()
                    else:      
                        for book in book_id:
                            book_id = book
                            b_bookid = str(book_id).encode('utf-8')
                            client.send(b"\n[+]  The LIST_ID is: " + b_bookid)
                        
                        client.send(b"\n\n[?] Do you want to mark a book as read from your reading list? Y or N [?]\n")
                        answer = client.recv(1024).decode('utf-8').rstrip()
                        if answer == "Y" or answer == "y":
                            while True:
                                time.sleep(1)
                                #client.send(b"\n")        
                                client.send(b"\n\n###  Which book have you read and would like to mark as read?\n")
                                client.send(b"###  Insert the LIST_ID number from the reading list above\n")
                                list_id = client.recv(1024).decode('utf-8').rstrip()

                                try:
                                    list_id = int(list_id)   
                                    cursor = conn.cursor()
                                    delete_book = "DELETE FROM read_list WHERE list_id = %s"
                                    cursor.execute(delete_book, (list_id,))
                                    conn.commit()
                                    b_listid = str(list_id).encode('utf-8')
                                    client.send(b"\n[+]  The list id of " + b_listid + b" has been marked as read" + b"\n")
                                    client.send(b"\n[+] Byeee, see you again!!")
                                    exit()
                                    break
                                except Exception as e:
                                    client.send(b"\n[-]  Please insert number only :(")

                            exit()
                        elif answer == "N" or answer == "n":
                            client.send(b"\n[+] Byeee, see you again!!")
                            exit()

                        # elif answer == "devutil":
                        #     client.send(b"\n[*] Which Readlyst file you would like to test? [*]\n")
                        #     file = client.recv(1024).decode('utf-8').rstrip()
                        #     p = Process(target=exec, args=(open(file).read(),))
                        #     p.start()
                        #     #exec(open(file).read())

                        else:
                            client.send(b"\n[-] Wrong input, Please select Y/y or N/n only!! Exiting..")
                            exit()

                else:
                    # if they are incorrect, exit the program
                    client.send(b"\n   Invalid email or password! Exiting!!\n")
                    exit()
            except ValueError:
                client.send(b"\n   Invalid format, please double check!! Exiting!!\n")
                exit()
            
    while True:
        client, addr = s.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

    #Close connection to MySQL database and socket
    conn.close()
    s.close()