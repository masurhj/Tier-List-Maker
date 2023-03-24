import pyorient
import json
client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "ich3aeNg")
print(session_id)

client.db_open("Library", "admin", "admin")
#client.command("CREATE VERTEX Book CONTENT {'Title': 1984, PageCount: '20'}")



print("welcome to the library!")
ADD_BOOK = "add book"
VIEW_BOOKS = "view books"
VIEW_BORROWER_BOOKS = "view borrower books"
DEL_BOOK = "del book"
EDIT_BOOK = "edit book"
VIEW_BORROWERS = "view borrowers"
ADD_BORROWER = "add borrower"
DEL_BORROWER = "del borrower"
EDIT_BORROWER = "edit borrower"
SEARCH_BORROWER = "search borrower"
SEARCH_BOOK = "search book"
CHECKOUT_BOOK = "checkout book"
CHECKIN_BOOK = "checkin book"
CHECK_BORROWER_BOOK_COUNT = "check borrower book count"


def bookExists(isbn):
    res = client.command("SELECT FROM BOOK WHERE ISBN='%s'" % (isbn))
    return len(res) > 0

def addBook():
    isbn = input("input isbn:\n")
    if (bookExists(isbn)):
        print("book with that isbn already exists")
        return
    else:
        title = input("input title: \n")
        pageCount = input("input page count (integer):\n")
        authorCount = input("how many authors (integer):\n")
        authors = [];
        for i in range(int(authorCount)):
            author = input("input author: " + str(i + 1) + "\n")
            authors.append(author)
        document = ({
            'Title': title,
            'ISBN' : isbn,
            'PageCount' : pageCount,
            'Authors' : authors,
            })
        result = client.command("CREATE VERTEX BOOK CONTENT " + json.dumps(document))
        #print('added ' + '"' + title + '"' + "with id : " + str(result.inserted_id))
        print('document is : ' + str(document))

def delBook():
    isbn = input("input isbn:\n")
    if (not bookExists(isbn)):
        print("book not found")
        return
    if (not bookAvailable(isbn)):
        print("book must first be checked in")
        return
    client.command("DELETE VERTEX BOOK WHERE ISBN='%s'" % (isbn))
    print("book deleted")

def editBook():
    isbn = input("input isbn of book to edit:\n")
    if (not bookExists(isbn)):
        print("no book with that isbn in catalog")
        return
    else:
        while(True):
            editField = input("what field would you like to edit? Title, ISBN, Authors, PageCount\n")
            if (editField == 'Title' or editField == 'ISBN' or editField == 'Authors' or editField == 'PageCount'):
                if (editField == "Authors"):
                    authCount = input("how many authors? (integer)")
                    authors = []
                    for i in range(int(authCount)):
                        author = input("input author: " + str(i + 1) + "\n")
                        authors.append(author)
                    client.command("UPDATE BOOK SET Authors=%s WHERE ISBN='%s'" % (authors, isbn))
                    break
                else:
                    newVal = input("what would you like to set the value as?\n")
                    client.command("UPDATE BOOK SET %s='%s' WHERE ISBN='%s'" % (editField, newVal, isbn))
                    break
            else:
                print("invalid field")

def viewBooks():
    sortBy = input("what would you like the books sorted by? (Title, PageCount, ISBN, Authors)\n")
    booksArr = []
    if (sortBy == "Title" or sortBy == "PageCount" or sortBy == "ISBN" or sortBy == "Authors"):
        booksArr = client.command("SELECT FROM BOOK ORDER BY %s ASC" % (sortBy))
    print("books sorted by " + sortBy + ":")
    printBooks(booksArr)

def viewBorrowerBooks():
    username = input("input username of borrower:\n")
    books = client.command("SELECT FROM (TRAVERSE * FROM (SELECT FROM BORROWER WHERE Username='%s')) WHERE @class = 'Book'" % (username))
    printBooks(books)

def printBooks(books):
    for book in books:
        print(book)

def printBorrowers(borrowers):
    for borrower in borrowers:
        print(borrower)

def viewBorrowers():
    borrowers = client.command("SELECT FROM BORROWER")
    printBorrowers(borrowers)

#TODO Fix search by authors
def searchBook():
    searchField = input("what would you like to search by? (Title, ISBN, Authors)\n")
    searchWith = input("enter a " + searchField + ":\n")
    if (searchField != 'Title' and searchField != 'ISBN' and searchField != 'Authors'):
        print('search field not supported')
        return
    booksArr = []
    booksArr = client.command("SELECT FROM BOOK WHERE %s='%s'" % (searchField, searchWith))
    for book in booksArr:
        print(book)

def borrowerExists(username):
    return len(client.command("SELECT FROM BORROWER WHERE Username='%s'" % (username))) > 0

def addBorrower():
    username = ""
    while(True):
        username = input("enter borrower username:\n")
        if (borrowerExists(username)):
            print("username already in use. Select a different one\n")
        else:
            break
    name = input("enter borrower name:\n")
    phone = input("enter borrower phone number:\n")
    borrower = ({
        "Username": username,
        "Phone": phone,
        "Name": name
        })
    client.command("CREATE VERTEX BORROWER CONTENT " + json.dumps(borrower))
    print("user added successfully")


#TODO: TEST ME
def delBorrower():
    #only let the borrower be deleted if all of their books are checked in
    username = input("input the username to delete:\n")
    if (not borrowerExists(username)):
        print("borrower not found")
        return
    if (len(client.command("SELECT FROM BORROWER WHERE Username='%s' AND (out_ is NULL or out_.size() < 1)" % (username))) < 1):
        print("borrower must first check in books")
        return
    client.command("DELETE VERTEX BORROWER WHERE Username='%s'" % (username))
    print("user deleted")


#TODO create separate cases for each attribute to add so that numbers are numbers and strings are strings
def editBorrower():
    username = input("input the username of the user to edit:\n")
    if (not borrowerExists(username)):
        print("user not found")
        return
    fieldToEdit = ""
    while(True):
        fieldToEdit = input("enter the field to edit (Username, Phone, or Name):\n")
        if (fieldToEdit != "Phone" and fieldToEdit != "Name" and fieldToEdit != "Username"):
            print("invalid field")
        else:
            break;
    newVal = input("input the new value for " + fieldToEdit + "\n")
    client.command("UPDATE BORROWER SET %s='%s' WHERE Username='%s'" % (fieldToEdit, newVal, username))
    print("value set")

def searchBorrower():
    searchField = input("what field would you like to search on (Name or Username)?\n")
    if (searchField != "Name" and searchField != "Username"):
        print("invalid field name")
        return
    searchVal = input("what " + searchField + " value would you like to search with?\n")
    borrowersArr = []
    borrowersArr = client.command("SELECT FROM BORROWER WHERE %s='%s'" % (searchField, searchVal))
    for borrower in borrowersArr:
        print(borrower)

def bookAvailable(isbn):
    return len(client.command("SELECT FROM BOOK WHERE ISBN='%s' AND (in_.size() < 1 OR in_.size() IS NULL)" % (isbn))) > 0

def checkoutBook():
    username = input("input username:\n")
    if (not borrowerExists(username)):
        print("user not found")
        return
    isbn = input("input book isbn:\n")
    if (not bookExists(isbn)):
        print("book not found")
        return
    if (not bookAvailable(isbn)):
        print("that book is not in stock")
        return
    client.command("CREATE EDGE FROM (SELECT FROM BORROWER WHERE Username='%s') TO (SELECT FROM BOOK WHERE ISBN='%s')" % (username, isbn))
    print("checkout successful")
    

#anyone can check in any book
def checkinBook():
    isbn = input("input book isbn:\n")
    if (not bookExists(isbn)):
        print("book not found")
        return
    if (bookAvailable(isbn)):
        print("book not checked out")
        return
    client.command("DELETE EDGE E WHERE @RID IN (SELECT in_ FROM BOOK WHERE ISBN='%s')" % (isbn))
    print("checkin successful")
    
#TODO: Fix me!
def checkBookCount():
    username = input("select user to view book count of\n")
    if (not borrowerExists(username)):
        print("user not found")
        return
    booksOut = client.command("SELECT out_.size() FROM Borrower WHERE Username='%s'" % (username))
    print(booksOut[0])

    

def listCommands():
    print("Enter any of the following commands:")
    print(VIEW_BOOKS)
    print(VIEW_BORROWER_BOOKS)
    print(ADD_BOOK)
    print(DEL_BOOK)
    print(EDIT_BOOK)
    print(VIEW_BORROWERS)
    print(ADD_BORROWER)
    print(DEL_BORROWER)
    print(EDIT_BORROWER)
    print(SEARCH_BOOK)
    print(SEARCH_BORROWER)
    print(CHECKOUT_BOOK)
    print(CHECKIN_BOOK)
    print(CHECK_BORROWER_BOOK_COUNT)

listCommands()
while True:
    cmd = input(">>> ")
    if (cmd == "help"):
        listCommands()
    elif (cmd == ADD_BOOK):
        addBook()
    elif (cmd == DEL_BOOK):
        delBook()
    elif (cmd == EDIT_BOOK):
        editBook()
    elif (cmd == VIEW_BOOKS):
        viewBooks()
    elif (cmd == SEARCH_BOOK):
        searchBook()
    elif (cmd == ADD_BORROWER):
        addBorrower()
    elif (cmd == DEL_BORROWER):
        delBorrower()
    elif (cmd == EDIT_BORROWER):
        editBorrower()
    elif (cmd == SEARCH_BORROWER):
        searchBorrower()
    elif (cmd == CHECKOUT_BOOK):
        checkoutBook()
    elif (cmd == CHECKIN_BOOK):
        checkinBook()
    elif (cmd == CHECK_BORROWER_BOOK_COUNT):
        checkBookCount()
    elif (cmd == VIEW_BOOKS):
        removeBookAttribute()
    elif (cmd == VIEW_BORROWERS):
        viewBorrowers()
    elif (cmd == VIEW_BORROWER_BOOKS):
        viewBorrowerBooks()
    elif (cmd == 'q'):
        break
    else:
        print("command not recognized. Type 'help' for a list of commands")




