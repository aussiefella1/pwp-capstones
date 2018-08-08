class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print ("The user with the name {name} has their email address to {email}".format(name = self.name, email = self.email))

    def __repr__(self):
        return "The user {name} with email address {email} has read {books} books.".format(name = self.name, email = self.email, books = len(self.books))

    def __eq__(self, other_user):
        return self.email == other_user.get_email() and self.name == other_user.get_name()

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        #iterate through all values in self.book and calculate average
        avg_rate = 0
        count = 0
        for v in self.books.values():
            if v != None:
                avg_rate += v
                count += 1
        return avg_rate / count

class Book(object):
    def __init__ (self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("The isbn for the book {book} has been changed to {isbn}".format(book = self.title, isbn = self.isbn))

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("You have provided an Invalid Rating.")

    def __eq__ (self, other_book):
        if other_book.title == self.title:
            return other_book.isbn == self.isbn

    def get_average_rating(self):
        #iterate through all values in self.ratings and calculate average
        average_rating = 0
        ratings_total = 0
        for rating in self.books.values():
            ratings_total += rating
        average_rating = ratings_total / len(self.books)
        return average_rating

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{title}, ISBN: {isbn}".format(title = self.title, isbn = self.isbn)

class Fiction(Book):
    def __init__ (self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}". format(title = self.title, level = self.level, subject = self.subject)

class TomeRater(object):

    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        if not self.isbn_duplicate(isbn):
            return Book(title, isbn)
        else:
            print("The isbn {isbn} exists already".format(isbn=isbn))

    def create_novel(self, title, author, isbn):
        if not self.isbn_duplicate(isbn):
            return Fiction(title, author, isbn)
        else:
            print("The isbn {isbn} exists already".format(isbn = isbn))

    def create_non_fiction(self, title, subject, level, isbn):
        if not self.isbn_duplicate(isbn):
            return Non_Fiction(title, subject, level, isbn)
        else:
            print("The isbn {isbn} exists already".format(isbn = isbn))

    def add_book_to_user(self, book, email, rating = None):
        if email not in self.users:
            print("There is no user with the {email} address.".format(email = email))
        else:
            user = self.users.get(email)
            user.read_book(book, rating)
            if book in self.books:
                self.books[book] = self.books.get(book) + 1
            else:
                self.books[book] = 1

    def add_user(self, name, email, user_books = None):
        if not self.valid_email(email):
            print("The {email} address provided is not valid".format(email = email))
            return
        if self.users.get(email) is None:
            user = User(name, email)
            self.users[email] = user
            if user_books is not None:
                for i in user_books:
                    self.add_book_to_user(i, email)
        else:
            print("The {email} address already has a user associated with it".format(email = email))

    def print_catalog(self):
        #iterate through all of the keys in self.books and then prints them
        for i in self.books:
            print(i)

    def print_users(self):
        #iterates through all of the values of self.users (which are the User objects), and prints them
        for i in self.users.values():
            print(i)

    def get_most_read_book(self):
        if self.books:
            max_read = max(self.books.values())
            return list(k for k, v in self.books.items() if v == max_read)
        return None

    def highest_rated_book(self):
        best = None
        highest_rating = 0
        for book in self.books.keys():
            if User.get_average_rating(self) > highest_rating:
                highest_rating = User.get_average_rating(self)
                best = book
        return best

    def most_positive_user(self):
        ratings = {}
        for user in self.users.values():
            ratings[user.name] = user.get_average_rating()
        maximum = max(ratings, key = ratings.get)
        print("User: {}\nScore: {}".format(maximum, ratings[maximum]))

    def isbn_duplicate(self, isbn):
        for i in self.books:
            if i.get_isbn() == isbn:
                return True
        return False

    def valid_email(self, email):
        if email.count("@") != 1:
            return False
        if email[-4:] not in ['.com','.edu', '.org']:
            return False
        return True

#Testing
