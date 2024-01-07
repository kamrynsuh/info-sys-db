import sqlite3
import re
import sqlite3
import ui
import Database

def artBoard():
    print("############# Art Gallery #############")

def createAccount():
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    ## Checking if there are 5 user accounts already
    cursor.execute("SELECT COUNT(*) FROM user")
    number = cursor.fetchall()

    if (len(number)) >= 5:
        print(
            "All permitted accounts have been created, please log in if you have an account."
        )

    else:
        username = single_line_alphaString("Enter Username (only alphabet): ")
        while checkUsernameExists(username):
            print("\nAn account of that username exists, try again.\n")
            username = single_line_alphaString("Enter Username:")

        password = single_line_string("Enter Account Password (must be 8-12 characters long, has a digit, capital letter, & special letter): ")
        while not checkPasswordWorks(password):
            password = single_line_string("Enter Account Password: ")

        firstName = single_line_alphaNumString("Enter First Name: ")
        lastName = single_line_alphaNumString("Enter Last Name: ")
        statusAcc = single_line_string("Enter Default or Core: ") #core membership: deviantart

        cursor.execute(
            """
        INSERT INTO user (username, password, first_name, last_name, tier_name) VALUES(?,?,?,?,?)""",
            (username, password, firstName, lastName, statusAcc),
        )
        db.commit()

        print("You have registered", username)

def checkUsernameExists(Username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_user = "SELECT * FROM user WHERE username = ?"
    cursor.execute(find_user, [(Username)])
    results = cursor.fetchall()
    cursor.close()

    if len(results) > 0:
        return True
    else:
        return False

def checkNameExists(me):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    first = input("Enter First Name: ")
    last = input("Enter Last Name: ")
    # Check if user is in system
    find_someone = "SELECT * FROM user WHERE first_name = ? AND last_name = ?"
    cursor.execute(find_someone, [(first), (last)])
    exist = cursor.fetchall()

    usernames = []
    for each in exist:
        usernames.append(each[1])

    if len(exist) > 0:
        print("Users with that name", first, last, ": ")
        for user in exist:
            print("Username: ", user[1], ", Name: ", user[3], " ", user[4])

        if wantSendRequest() == True:
            requested = single_line_alphaNumString("Enter their username: ")
            if requested in usernames:
                friend_request(me, requested)
            else:
                print("That isn't their username.")
    else:
        print("They are not apart of the DailyArt system yet")

def listByUserName(me):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    user = input("Enter Username: ")
    # Check if user is in system
    find_someone = "SELECT * FROM user WHERE username = ?"
    cursor.execute(find_someone, [(user)])
    exist = cursor.fetchall()

    usernames = []
    for each in exist:
        usernames.append(each[1])

    if len(exist) > 0:
        for user in exist:
            print("Username: ", user[1], ", Name: ", user[3], " ", user[4])

        if wantSendRequest() == True:
            requested = single_line_alphaNumString("Enter their username: ")
            if requested in usernames:
                friend_request(me, requested)
            else:
                print("That isn't one of the usernames.")

    else:
        print("They are not yet a part of the DailyArt system yet")

def login_credentials():
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    username = single_line_alphaString("\nUsername: ")
    password = single_line_string("Password: ")

    find_user = "SELECT * FROM user WHERE username = ? AND password = ?"
    cursor.execute(find_user, [(username), (password)])
    results = cursor.fetchall()

    if results:
        return [True, username]
    else:
        return [False]

# creating your own profile main function
def createUserProfile(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    user_count = ("SELECT * FROM profiles WHERE username = ?")
    cursor.execute(user_count, [(username)])
    number = cursor.fetchall()

    if (len(number)) > 0:
        print(
            "You already have a profile, but you can use the edit option!"
        )
    else:
        title = (input("Enter your level (E.g., Hobbyist, Professional, Student, None): ")).title()
        location = (input("Enter your location: ")).title()
        specialty = (input("Enter your specialty (E.g., Digital Art, Traditional Art, Photography, None): ")).title()
        about = multi_line_string("Write your bio: ")

        cursor.execute(
            """
        INSERT INTO profiles (username, title, location, specialty, about) VALUES(?,?,?,?,?)""",
            (username, title, location, specialty, about),
        )
        db.commit()
        print("Your profile has been created.")

# edit user profile main function
def editUserProfile(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    profile_count = ("SELECT * FROM profiles WHERE username = ?")
    cursor.execute(profile_count, [(username)])
    number = cursor.fetchall()

    for i in number:
        print("PROFILE: ", i)

    if (len(number)) == 0:
        print(
            "You haven't created a profile yet"
        )
    else:
        print(ui.edit_profile_menu)
        edit_option = integer_in_range("Enter which to edit: ", 1, 5, ui.edit_profile_menu)

        while (edit_option != 5):

            if edit_option == 1:
                change = (input("Enter your title (E.g., Student): ")).title()
                update = ''' UPDATE profiles SET title = ? WHERE username = ?'''

            elif edit_option == 2:
                change = (input("Enter your location: ")).title()
                update = ''' UPDATE profiles SET location = ? WHERE username = ?'''

            elif edit_option == 3:
                change = (input("Enter your specialty: ")).title()
                update = ''' UPDATE profiles SET specialty = ? WHERE username = ?'''

            else:
                change = multi_line_string("Rewrite your bio: ")
                update = ''' UPDATE profiles SET about = ? WHERE username = ?'''

            cursor.execute(update, [change, username])
            print("Finished editing your user profile")
            db.commit()

            print(ui.edit_profile_menu)
            edit_option = integer_in_range("Enter which to edit: ", 1, 5, ui.edit_profile_menu)

# create/sell art on market function
def createArt(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    art_count = ("SELECT * FROM art WHERE username = ?")
    cursor.execute(art_count, [(username)])
    number = cursor.fetchall()

    # limits user to 10 art pieces to post
    if (len(number)) >= 10:
        print(
            "You have listed the max amount of artwork."
        )
    else:
        title = (single_line_string("Enter your artwork title: ")).title()
        year = integer("Enter the year it was made: ")
        medium = single_line_string("Enter the medium you used: ")
        price = integer("Enter your pricing (integer only): ")
        description = multi_line_string("Enter a description of the artwork: ")

        cursor.execute(
            """
        INSERT INTO art (username, title, year, medium, price, description) VALUES(?,?,?,?,?,?)""",
            (username, title, year, medium, price, description),
        )
        db.commit()
        print("Your artwork has been listed.")

#main function to edit art piece
def editArt(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    edit_art = ("SELECT * FROM art WHERE username = ?")
    cursor.execute(edit_art, [(username)])
    number = cursor.fetchall()

    if (len(number)) == 0:
        print(
            "You have not listed any artwork yet."
        )
    else:
        displayUserArt(username)
        artTitle = chooseArt(username)

        print(ui.edit_art_menu)
        edit_option = integer_in_range("Enter which to edit: ", 1, 6, ui.edit_art_menu)

        while (edit_option != 6):

            if edit_option == 1:
                change = (single_line_string("Enter your artwork title: ")).title()
                update = ''' UPDATE art SET title = ? WHERE username = ? AND title = ?'''

            elif edit_option == 2:
                change = integer("Enter the year it was made: ")
                update = ''' UPDATE art SET year = ? WHERE username = ? AND title = ?'''

            elif edit_option == 3:
                change = single_line_string("Enter the medium you used: ")
                update = ''' UPDATE art SET medium = ? WHERE username = ? AND title = ?'''

            if edit_option == 4:
                change = integer("Enter your pricing (integer only): ")
                update = ''' UPDATE art SET price = ? WHERE username = ? AND title = ?'''

            elif edit_option == 5:
                change = multi_line_string("Enter your description: ")
                update = ''' UPDATE art SET description = ? WHERE username = ? AND title = ?'''

            cursor.execute(update, [change, username, artTitle])
            db.commit()

            print(ui.edit_art_menu)
            edit_option = integer_in_range("Enter which to edit: ", 1, 6, ui.edit_art_menu)

# function to edit art piece
def chooseArt(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    art_count = ("SELECT * FROM art WHERE username = ?")
    cursor.execute(art_count, [(username)])
    number = cursor.fetchall()

    print("Select one of the following to edit: ")
    a = 1
    for result in number:
        print(a, ". ", result[2])
        a = a + 1

    choice = integer_in_range("Select one of the artworks to edit by number: ", 1, len(number), "NULL")
    return (number[choice - 1][2])

# display any user profile, main function
def displayUser(me, username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_user = "SELECT * FROM profiles WHERE username = ?"
    cursor.execute(find_user, [(username)])
    profiles = cursor.fetchall()

    find_user = "SELECT * FROM art WHERE username = ?"
    cursor.execute(find_user, [(username)])
    art = cursor.fetchall()

    if len(profiles) > 0:
        displayUserProfile(username)
    else:
         print("The user you're trying to display the profile for, does not have a profile yet. Try again later.")


def displayUserProfile(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_user = "SELECT * FROM user WHERE username = ?"
    cursor.execute(find_user, [(username)])
    users = cursor.fetchall()

    find_profile = "SELECT * FROM profiles WHERE username = ?"
    cursor.execute(find_profile, [(username)])
    profiles = cursor.fetchall()

    for user in users:
        print("\n---------- You are viewing ", user[3], user[4],"'s profile ----------")
        print("Title: ", profiles[0][2])
        print("Location: ", profiles[0][3])
        print("Specialty: ", profiles[0][4])
        print("About: ", profiles[0][5])

def displayUserArt(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_art = "SELECT * FROM art WHERE username = ?"
    cursor.execute(find_art, [(username)])
    results = cursor.fetchall()

    for art in results:
        print("\n---------- Artworks ----------")
        print("Title: ", art[2])
        print("Year: ", art[3])
        print("Medium: ", art[4])
        print("Price: ", art[5])
        print("Description of artwork: ", art[6])

def listAllUsers():
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    cursor.execute("SELECT * FROM user")
    results = cursor.fetchall()

    print("Existing Accounts (for demo purposes):")
    number = 1
    for i in results:
        print(f"  {number}: {i[1]}")
        number = number + 1

    cursor.close()

def friend_request(me, stranger):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    if checkUsernameExists(stranger) == False:
        print("The username you try to add as friend does not exist.")
        return

    find_request = "SELECT * FROM friends WHERE username = ? AND stranger = ?"
    cursor.execute(find_request, [(me), (stranger)])
    exist = cursor.fetchall()
    if len(exist) > 0:
        print("You've already sent a friend request to this user.")
        db.close()
        return

    cursor.execute(
        """
    INSERT INTO friends (username, stranger, status) VALUES(?,?,'sentpending')""",
        (me, stranger),
    )
    cursor.execute(
        """
    INSERT INTO friends (username, stranger, status) VALUES(?,?,'acceptpending')""",
        (stranger, me),
    )
    db.commit()
    print("You Have sent friend request to", stranger)

def exec_friend_request(me):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_acceptRequests = "SELECT * FROM friends WHERE username = ? AND status = 'acceptpending'"
    cursor.execute(find_acceptRequests, [(me)])
    results = cursor.fetchall()

    for sent in results:

        stranger = sent[1]
        print("\nWould you like to accept friend request from", stranger)
        FriendChoice = integer_in_range(
            "Enter 1 to Accept and 2 to Reject: ", 1, 2, "NULL"
        )
        if FriendChoice == 2:
            # delete both users' request from db
            reject_request = "DELETE FROM friends WHERE username = ? AND stranger = ?"
            cursor.execute(reject_request, [(me), (stranger)])
            reject_request2 = "DELETE FROM friends WHERE username = ? AND stranger = ?"
            cursor.execute(reject_request2, [(stranger), (me)])
            db.commit()
            print("You have rejected friend request from", stranger)
            db.close()
        else:
            # both change status to "friend"
            reject_request1 = ''' UPDATE friends SET status = ? WHERE username = ? AND stranger = ?'''
            cursor.execute(reject_request1, [("friend"), (me), (stranger)])
            reject_request2 = ''' UPDATE friends SET status = ? WHERE username = ? AND stranger = ?'''
            cursor.execute(reject_request2, [("friend"), (stranger), (me)])
            db.commit()
            print("You have accepted friend request from,", stranger)
            db.close()

def delete_friend(me, stranger):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    # delete both users' request from database
    reject_request = "DELETE FROM friends WHERE username = ? AND stranger = ?"
    cursor.execute(reject_request, [(me), (stranger)])
    reject_request2 = "DELETE FROM friends WHERE username = ? AND stranger = ?"
    cursor.execute(reject_request2, [(stranger), (me)])
    db.commit()
    print("You have removed ", stranger)
    db.close()

def listPending(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_sentRequests = "SELECT * FROM friends WHERE username = ? AND status = 'sentpending'"
    cursor.execute(find_sentRequests, [(username)])
    results = cursor.fetchall()

    print("Your outgoing friend requests:")
    for sent in results:
         print(sent[1])

    find_acceptRequests = "SELECT * FROM friends WHERE username = ? AND status = 'acceptpending'"
    cursor.execute(find_acceptRequests, [(username)])
    results = cursor.fetchall()

    print("Your incoming friend requests: \n")
    for sent in results:
        print(sent[0])

def listFriends(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_friends = "SELECT * FROM friends WHERE username = ? AND status = 'friend'"
    cursor.execute(find_friends, [(username)])
    results = cursor.fetchall()

    usernames = []
    for each in results:
        usernames.append(each[1])

    if len(results) > 0:
        print("Your friends:")
        for sent in results:
            print("     ", sent[1])

        if wantDeleteFriend() == True:
            requested = single_line_alphaNumString("Enter their username: ")
            if requested in usernames:
                delete_friend(username, requested)
            else:
                print("That isn't one of the usernames.")
    else:
        print("You don't have any connections.")

def checkFriends(username, friend):
    print("Check friends: ", username, friend)
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_friends = "SELECT * FROM friends WHERE username = ? AND status = 'friend'"
    cursor.execute(find_friends, [(username)])
    results = cursor.fetchall()

    if len(results) > 0:
        return True
    else:
        return False

def pending_friend(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_pending = "SELECT * FROM friends WHERE username = ? AND status = 'acceptpending'"
    cursor.execute(find_pending, [(username)])
    pending = cursor.fetchall()
    if len(pending) > 0:
        return True
    else:
        return False

# delete/unlist art you put on market
def deleteArt(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    art_count = ("SELECT * FROM art WHERE username = ?")
    cursor.execute(art_count, [(username)])
    number = cursor.fetchall()

    if (len(number)) == 0:
        print(
            "You haven't listed an artwork yet."
        )
    else:
        displayUserArt(username)
        print("Select one of the following to delete: ")
        a = 1
        for result in number:
            print(a, ". ", result[2])
            a = a + 1
        choice = integer_in_range("Select one of the artworks to delete by number: ", 1, len(number), "NULL")
        artTitle = (number[choice - 1][2])  # number 2d list

        delete_arts = "DELETE FROM art WHERE username = ? AND title = ?"
        cursor.execute(delete_arts, [(username), (artTitle)])
        db.commit()

        find_status = "SELECT * FROM buyInfo WHERE title = ?"
        cursor.execute(find_status, [(artTitle)])
        find_results = cursor.fetchall()

        if len(find_results) > 0:
            update_status = ''' UPDATE buyInfo SET status = ? WHERE title = ?'''
            cursor.execute(update_status, [("deleted"), (artTitle)])
            db.commit()

        print("This artwork has been deleted: ", artTitle)
        db.close()

# deletion function
def deletion_detector(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_deleted = "SELECT * FROM buyInfo WHERE username = ? AND status = 'deleted'"
    cursor.execute(find_deleted, [(username)])
    deleted = cursor.fetchall()
    if len(deleted) > 0:
        print("NOTIFICATION: Unfortunately, following artwork(s) you purchased for has been deleted by the artist: ")
        for art in deleted:
            print("Title: ", art[1])

#list of art you have purchased
def listArtPurchases(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_artPurchased = "SELECT * FROM buyInfo WHERE username = ? AND status = 'applied'"
    cursor.execute(find_artPurchased, [(username)])
    results = cursor.fetchall()
    if len(results) > 0:
        for applied in results:
            print("Title: ", applied[2])
    else:
        print("You have no purchased art prints in your list. Try purchasing one and looking back here again!")

# count how much art you have purchased
def CountArt(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_artPurchased = "SELECT * FROM buyInfo WHERE username = ? AND status = 'applied'"
    cursor.execute(find_artPurchased, [(username)])
    results = cursor.fetchall()

    art_count = 0
    print("Your purchased artworks: \n")
    for applied in results:
        art_count = art_count + 1;

    return art_count

# unfavorite art
def unsaveArt(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    choice2 = integer_in_range("\nDo you want to unfavorite any artwork in your list?"
                               "\n1. Unfavorite the artwork"
                               "\n2. Back to main menu"
                               "\nType 1 or 2 here: ", 1, 2, "NULL")
    if choice2 == 1:
        title1 = (single_line_string("Enter the artwork title you want to unfavorite: ")).title()

        delete_save = "DELETE FROM buyInfo WHERE username = ? AND title = ? AND status = 'saved'"
        cursor.execute(delete_save, [(username), (title1)])
        db.commit()

        print("This artwork has been unfavorited.")
        db.close()

# list of all favorited works
def listArtSaved(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_ArtSaved = "SELECT * FROM buyInfo WHERE username = ? AND status = 'saved'"
    cursor.execute(find_ArtSaved, [(username)])
    results = cursor.fetchall()

    if len(results) > 0:
        print("Your favorite artworks: \n")
        for saved in results:
            print("Title: ", saved[2])
            unsaveArt(username)
    else:
        print("You haven't favorited any artworks.")

# you can buy multiple art prints, that is why it remains in the db and theres no delete function
def buyArt(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()
    buying_art = ("SELECT * FROM art")
    cursor.execute(buying_art)
    number = cursor.fetchall()

    if (len(number)) > 0:
        a = 1
        for arts in number:
            print(a, ".", arts[2])
            a = a + 1
        choice = integer_in_range("\nSelect one of the artworks by number to purchase: ", 1, len(number), "NULL")
        buy_art = ("SELECT * FROM buyInfo WHERE username = ? AND title = ? AND status = 'applied'")
        cursor.execute(buy_art, [(username), (number[choice - 1][2])])
        number2 = cursor.fetchall()

        if (len(number2)) > 0:
            print("You have already purchased, try purchasing for another artwork.")
        elif (username == number[choice - 1][1]):
            print(
                "You cannot purchase an artwork you have created yourself, try purchasing for another artwork that you haven't created.")
        else:
            #title = (single_line_string("Enter the title of the artwork: ")).title()
            price = integer("Enter your pricing (integer only): ")
            payment = single_line_string("Enter the payment option (E.g., Paypal, Cashapp, etc) : ")
            comment = multi_line_string("Enter any additional comments/special requests: ")

            cursor.execute(
                """
            INSERT INTO buyInfo (username, title, price, payment, comment, status) VALUES(?,?,?,?,?,'applied')""",
                (username, number[choice - 1][2], price, payment, comment),
            )
            db.commit()
            print("Your offer has been made.")
            db.close()
    else:
        print("There are no art prints in the gallery right now to buy. Check again later.")

# favoriting art
def saveArt(username, choice):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_art = "SELECT * FROM art"
    cursor.execute(find_art)
    results = cursor.fetchall()

    choice2 = integer_in_range("\nDo you want to favorite this artwork to your list?"
                               "\n1. Favorite the artwork"
                               "\n2. Back to main menu"
                               "\nType 1 or 2 here: ", 1, 2, "NULL")
    if choice2 == 1:
        find_favart = "SELECT * FROM buyInfo WHERE username = ? AND title = ? AND status ='saved'"
        cursor.execute(find_favart, [(username), (results[choice - 1][1])])
        st = cursor.fetchall()
        if len(st) > 0:
            print("You have already favorited it.")
        else:
            cursor.execute(
                """
            INSERT INTO buyInfo (username, title, status) VALUES(?,?,'saved')""",
                (username, results[choice - 1][2]),
            )
            db.commit()
            print("The artwork is favorited!")

# art gallery main interface
def artBoard(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    art_board = ("SELECT * FROM art")
    cursor.execute(art_board)
    number = cursor.fetchall()

    deletion_detector(username)  # notification

    art_counter = CountArt(username)

    print("✣✤❈ꕥ❈✤✣ Art Gallery ✣✤❈ꕥ❈✤✣")
    print("You have currently purchased", art_counter, "art print(s). Feel free to purchase more!")
    if (len(number)) == 0:
        print("No artworks have been posted")
    else:
        a = 1
        for art in number:
            print(a, ".", art[2])
            a = a + 1

        choice = integer_in_range("\nSelect one of the artworks by number to learn more about: ", 1, len(number), "NULL")
        print("Title: ", number[choice - 1][2])
        print("Year: ", number[choice - 1][3])
        print("Medium: ", number[choice - 1][4])
        print("Price: ", number[choice - 1][5])
        print("Description: ", number[choice - 1][6])
        saveArt(username, choice)

# can SEND and RECEIVE messages from people who have accepted their friend request
def defaultTier(sender, receiver):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    # Checking if they have them as a friend
    find_friends = "SELECT * FROM friends WHERE username = ? AND stranger = ? AND status = 'friend'"
    cursor.execute(find_friends, [(sender), (receiver)])
    results = cursor.fetchall()

    usernames = []
    for each in results:
        usernames.append(each[1])

    if len(results) > 0:
        print("These are your friends that you can message:")
        for sent in results:
            print("     ", sent[1])

        chatInput = input("Enter your message: ")

        cursor.execute(
            """
        INSERT INTO messageFriend (sender, receiver, message, status) VALUES(?,?,?,'sent')""",
            (receiver, sender, chatInput),
        )

        db.commit()
        print("You Have sent the message to", receiver)
        db.close()
    else:
        print("I'm sorry, you are not friends with that person.")


# can SEND and RECIEVE messages from people who have accepted their friend request
# can also SEND and RECEIVE messages from people not in thier friend list
def coreTier(sender):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    EveryOne = "SELECT * FROM user EXCEPT SELECT * FROM user WHERE username = ?"
    cursor.execute(EveryOne, [(sender)])
    results = cursor.fetchall()

    usernames = []
    for each in results:
        usernames.append(each[1])

    if len(results) > 0:
        print("These are the users that you can message:")
        for sent in results:
            print("     ", sent[1])
        user = input("Enter the user you want to message: ")
        chatInput = input("Enter your message: ")

        cursor.execute(
            """
            INSERT INTO messageFriend (sender, receiver, message, status) VALUES(?,?,?,'sent')""",
            (user, sender, chatInput),
        )

        db.commit()
        print("You Have sent the message to", user)
        db.close()
    else:
        print("Please try again.")

# Message notification
def message_detector(sender, receiver):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_message = "SELECT * FROM messageFriend WHERE sender = ? AND status = 'sent'"
    cursor.execute(find_message, [(sender)])
    results = cursor.fetchall()
    for msg in results:
        who = msg[1]
        print("NOTIFICATION: You have received a message from", who)

        readMsg = integer_in_range("\nPress 1 to read the message: ", 1, 1,"NULL")
        if readMsg == 1:
            print("Message: ", msg[2])  # display message
        else:
            db.close()
            #main()

        ## this part give user option (1 = leave it as it is, 3 = delete message from messsageTable, 2 = send message back)
        msgChoice = integer_in_range("Enter 1 to leave the message, 2 to send message back, 3 to delete the message: ",
                                     1, 3, "NULL")
        if msgChoice == 3:
            # delete the message from db
            reject_message = "DELETE FROM messageFriend WHERE sender = ?"
            cursor.execute(reject_message, [(sender)])
            db.commit()
            print("You have removed the message from your inbox")
            db.close()
            main()
        elif msgChoice == 2:
            friend = input("Name of the friend to send a message to: ")

            chatInput = input("Enter your message: ")

            cursor.execute(
                """
                INSERT INTO messageFriend (sender, receiver, message, status) VALUES(?,?,?,'sent')""",
                (friend, sender, chatInput),
            )

            db.commit()
            print("You Have sent the message to", friend)
            reject_message = "DELETE FROM messageFriend WHERE sender = ?"
            cursor.execute(reject_message, [(sender)])
            db.commit()
            db.close()
            main()
            message_detector(sender, receiver)
        else:
            print("You have left the message inside of your inbox. Come back again!")
            db.close()
            main()

def pending_message(username):
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    find_pending = "SELECT * FROM messageFriend WHERE sender = ? AND status = 'sent'"
    cursor.execute(find_pending, [(username)])
    pending = cursor.fetchall()
    if len(pending) > 0:
        return True
        # db.close()
    else:
        return False
        # db.close()

# UI Functions
def login_menu():
    print(ui.main_menu)
    choice = integer_in_range("Choice: ", 1, 5, ui.main_menu)
    return choice

# validation of password
def checkPasswordWorks(password):
    SpecialSymbol = ["$", "@", "#", "%", "!", "^", "&", "*"]
    if len(password) < 8 or len(password) > 12:
        print("Password Must be 8 - 12 Characters Long \n")
        return False
    elif not any(char.isdigit() for char in password):
        print("Make Sure Your Password has a Digit in it \n")
        return False
    elif not any(char.isupper() for char in password):
        print("Make Sure that the Password has a Capital Letter in it \n")
        return False
    elif not any(char in SpecialSymbol for char in password):
        print("Make Sure that the Password has a Special Letter in it \n")
        return False
    else:
        return True

# Input validation
def integer_in_range(prompt, low, high, menu):
    number = input(prompt)

    while (not number.isnumeric()) or (int(number) < low) or (int(number) > high):
        print("\nPlease select a valid option.")

        if menu != "NULL":
            print(menu)

        number = input(prompt)

    return int(number)

def integer(prompt):
    number = input(prompt)

    while not number.isnumeric():
        print("\nPlease select a valid option.\n")
        number = input(prompt)

    return int(number)

## This string input can have ANY characters EXCEPT spaces
def single_line_string(prompt):
    string_in = input(prompt)

    while " " in string_in:
        print("\nPlease type a valid response.\n")
        string_in = input(prompt)

    return string_in

## This string input can NOT have any numerical characters
def single_line_alphaString(prompt):
    string_in = input(prompt)

    while not string_in.isalpha():
        print("\nPlease type a valid response.\n")
        string_in = input(prompt)

    return string_in

def tryAgain():
    string_in = input("Would you like to try again? (Yes / No): ")
    acceptable = ["yes", "y", "no", "n"]

    while (not string_in.isalpha()) or (string_in.lower() not in acceptable):
        print("\nPlease type a valid response.\n")
        string_in = input("Would you like to try again? (Yes / No): ")

    if string_in.lower() == "yes" or string_in.lower() == "y":
        return True
    else:
        return False

def wantSendRequest():
    string_in = input("Would you like to send a friend request? (Yes / No): ")
    acceptable = ["yes", "y", "no", "n"]

    while (not string_in.isalpha()) or (string_in.lower() not in acceptable):
        print("\nPlease type a valid response.\n")
        string_in = input("Would you like to send a friend request? (Yes / No): ")

    if string_in.lower() == "yes" or string_in.lower() == "y":
        return True
    else:
        return False

def wantDeleteFriend():
    string_in = input("Would you like to remove a connection? (Yes / No): ")
    acceptable = ["yes", "y", "no", "n"]

    while (not string_in.isalpha()) or (string_in.lower() not in acceptable):
        print("\nPlease type a valid response.\n")
        string_in = input("Would you like to remove a connection? (Yes / No): ")

    if string_in.lower() == "yes" or string_in.lower() == "y":
        return True
    else:
        return False

## This string input CAN have any numerical characters
def single_line_alphaNumString(prompt):
    string_in = input(prompt)

    while not string_in.isalnum():
        print("\nPlease type a valid response.\n")
        string_in = input(prompt)

    return string_in

## This takes in any amount of lines - Any characters are valid
def multi_line_string(prompt):
    string_in = input(prompt)
    string_in += "\n"
    temp = " "

    while not (temp == ""):
        temp = input("")
        string_in += temp

    return string_in

# Main deal
def main():
    with sqlite3.connect("User.db") as db:
        cursor = db.cursor()

    cursor.execute("SELECT * FROM user")
    results = cursor.fetchall()

    # main ui
    print(ui.data_us)
    option = login_menu()

    # login
    if option == 1:
        listAllUsers()

        TryAgain = True
        while TryAgain == True:
            LoggedIn = login_credentials()
            if LoggedIn[0]:
                TryAgain = False
            else:
                TryAgain = tryAgain()

        if LoggedIn[0]:
            temp = LoggedIn[1]
            temp1 = "string"
            if pending_friend(LoggedIn[1]):
                print("You received a friend request.")
                exec_friend_request(LoggedIn[1])
            elif pending_message(temp):
                print("You have received a message in your inbox.")
                message_detector(temp, temp1)
            print(ui.logged_in_menu)
            choice = integer_in_range("Pick an Option: ", 1, 16, ui.logged_in_menu)
            while choice != 16:

                if choice == 1:  # Buy an Artwork
                    buyArt(LoggedIn[1])

                elif choice == 2:  # Sell an Artwork
                    createArt(LoggedIn[1])

                elif choice == 3: # search for artwork
                    artBoard(LoggedIn[1])

                elif choice == 4:  # List of Artworks on Market
                    print(ui.list_art_menu)
                    search_choice = integer_in_range("Select what you would like to search by: ", 1, 2,
                                                     ui.list_art_menu)
                    while search_choice != 2:
                        if search_choice == 1:
                            listArtPurchases(LoggedIn[1])

                        print(ui.list_art_menu)
                        search_choice = integer_in_range("Select what you would like to search by: ", 1, 2, "NULL")

                elif choice == 5:  # List of Favorite Artworks
                    listArtSaved(LoggedIn[1])

                elif choice == 6: #create a profile
                    createUserProfile(LoggedIn[1])

                elif choice == 7: #edit your profile
                    editUserProfile(LoggedIn[1])

                elif choice == 8: #Display a User Profile
                    userRequested = single_line_alphaString(
                        'Type the username of the user you want to see the profile for or "exit" to return: '
                    )
                    while (
                            not checkUsernameExists(userRequested)
                    ) and userRequested.lower() != "exit":
                        print(
                            "That username isn't in the system. Try again or type exit to leave.\n"
                        )
                        userRequested = single_line_alphaString(
                            'Type the username of the user you want to see the profile for or "exit" to return: '
                        )

                    if userRequested.lower() != "exit":
                        displayUser(LoggedIn[1], userRequested)

                elif choice == 9: #Edit Artwork Information
                    editArt(LoggedIn[1])

                elif choice == 10: #Unlist an Artwork
                    deleteArt(LoggedIn[1])

                elif choice == 11:  # Send a Friend Request
                    stranger = single_line_alphaNumString("Enter the username of the user you want to friend: ")
                    friend_request(LoggedIn[1], stranger)

                elif choice == 12:  # List Pending Requests
                    listPending(LoggedIn[1])

                elif choice == 13:  # Show My Network
                    listFriends(LoggedIn[1])
                elif choice == 14:  # Message
                    print(ui.message_menu)
                    search_choice = integer_in_range(
                        "Enter 1 as a Default member, Enter 2 as a Core member, Enter 3 to go back: ", 1, 3,
                        ui.message_menu)
                    while search_choice != 3:
                        if search_choice == 1:
                            receiver = single_line_alphaNumString(
                                "Enter the username of the user you want to send a message to: ")
                            defaultTier(LoggedIn[1], receiver)
                        elif search_choice == 2:
                            #receiver = single_line_alphaNumString("Enter the username of the user you want to send a message to: ")
                            # plusTier(LoggedIn[1], receiver)
                            coreTier(LoggedIn[1])
                        print(ui.message_menu)
                        search_choice = integer_in_range("Select what you would like to search by: ", 1, 3, "NULL")

                elif choice == 15: # Find Someone That You May Know
                    print(ui.search_menu)
                    search_choice = integer_in_range("Select what you would like to search by: ", 1, 3, "NULL")
                    while (search_choice != 3):
                        if search_choice == 1:
                            checkNameExists(LoggedIn[1])
                        elif search_choice == 2:
                            listByUserName(LoggedIn[1])

                        print(ui.search_menu)
                        search_choice = integer_in_range("Select what you would like to search by: ", 1, 3, "NULL")


                print(ui.logged_in_menu)
                choice = integer_in_range(
                    "Pick an Option: ", 1, 16, ui.logged_in_menu
                )

        print("You have left DailyArt. Come back again!")
        raise SystemExit(0)

    # create your acc
    if option == 2:
        createAccount()
        main()

    if option == 3:
        exit()

if __name__ == "__main__":
    main()
