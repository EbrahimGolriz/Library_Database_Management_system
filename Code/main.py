#   DESKTOP-3KLDFB9     LibraryDB
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QSizePolicy, QHBoxLayout
from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QStackedWidget,QTableWidgetItem,QTableWidget
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QDialog, QComboBox
from datetime import date
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from dotenv import load_dotenv
import time,os



# Define the database connection string
# db_connection_string = 'mssql+pyodbc://DESKTOP-3KLDFB9/LibraryDB?driver=ODBC+Driver+17+for+SQL+Server'
load_dotenv(".env")


db_server = os.environ.get("DB_SERVER")
db_name = os.environ.get("DB_NAME")

# Construct the connection string for Trusted Connection (Windows Authentication)
db_connection_string = f'mssql+pyodbc://{db_server}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server'


# Create the SQLAlchemy engine using PyODBC
db_engine = create_engine(db_connection_string)

# Create metadata
metadata = MetaData()

managers_table = Table('managers', metadata, autoload_with=db_engine)
customers_table = Table('customers', metadata, autoload_with=db_engine)
books_table = Table('books', metadata, autoload_with=db_engine)
customers_books_table = Table('customers_books', metadata, autoload_with=db_engine)
customers_books_history_table = Table('customers_books_history', metadata, autoload_with=db_engine)


class IntegerTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        return int(self.text()) < int(other.text())

class ManagerLoginPage(QWidget):
    def __init__(self, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.init_ui()

    def init_ui(self):


        label_style = "font-size: 18px;" 
        line_edit_style = "font-size: 16px; height: 30px;" 
        button_style = "font-size: 18px; height: 40px;border-radius: 10px;" 

        self.label_id = QLabel('ID:')
        self.label_id.setStyleSheet(label_style)
        
        self.label_password = QLabel('Password:')
        self.label_password.setStyleSheet(label_style)

        self.line_edit_id = QLineEdit()
        self.line_edit_id.setStyleSheet(line_edit_style)
        self.line_edit_id.setFixedSize(250, 30)

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setStyleSheet(line_edit_style)
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        self.line_edit_password.setFixedSize(250, 30) 

        self.button_enter = QPushButton('Enter')
        self.button_enter.setStyleSheet(f"background-color: green; color: white; {button_style}")
        self.button_enter.setFixedSize(250, 40) 
        self.button_enter.clicked.connect(self.login)

        self.button_back = QPushButton('Back')
        self.button_back.setStyleSheet(f"background-color: orange; color: black; {button_style}")
        self.button_back.setFixedSize(250, 40) 
        self.button_back.clicked.connect(self.back)


        layout = QVBoxLayout()
        layout.addWidget(self.label_id)
        layout.addWidget(self.line_edit_id)
        layout.addWidget(self.label_password)
        layout.addWidget(self.line_edit_password)
        layout.addWidget(self.button_enter)
        layout.addWidget(self.button_back)


        layout.setAlignment(Qt.AlignCenter) 

        self.setLayout(layout)

    def back(self) :
        self.page_controller.show_choose_login_page()
    def login(self):
        try:
            entered_id = int(self.line_edit_id.text())
        except ValueError:
            QMessageBox.warning(self, 'Login Status', 'ID must be a number.')
            self.line_edit_id.clear()
            return

        entered_password = self.line_edit_password.text()

        try:
            with db_engine.connect() as connection:
                query = select(managers_table).where(
                    (managers_table.c.m_id == entered_id) & (managers_table.c.m_password == entered_password)
                )
                result = connection.execute(query).fetchall()

                if len(result) > 0:
                    QMessageBox.information(self, 'Login Status', 'Welcome!')
                    self.page_controller.managermainpage.manager_id = entered_id
                    self.page_controller.show_manager_main_page()
                else:
                    QMessageBox.warning(self, 'Login Status', 'User not found.')
                    self.line_edit_id.clear()
                    self.line_edit_password.clear()

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

class CustomerLoginPage(QWidget):
    def __init__(self, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.init_ui()

    def init_ui(self):

        label_style = "font-size: 18px;" 
        line_edit_style = "font-size: 16px; height: 30px;"  
        button_style = "font-size: 18px; height: 40px;border-radius: 10px;"  

        self.label_id = QLabel('ID:')
        self.label_id.setStyleSheet(label_style)
        
        self.label_password = QLabel('Password:')
        self.label_password.setStyleSheet(label_style)

        self.line_edit_id = QLineEdit()
        self.line_edit_id.setStyleSheet(line_edit_style)
        self.line_edit_id.setFixedSize(250, 30) 

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setStyleSheet(line_edit_style)
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        self.line_edit_password.setFixedSize(250, 30)  

        self.button_enter = QPushButton('Enter')
        self.button_enter.setStyleSheet(f"background-color: green; color: white; {button_style}")
        self.button_enter.setFixedSize(250, 40)  
        self.button_enter.clicked.connect(self.login)

        self.button_back = QPushButton('Back')
        self.button_back.setStyleSheet(f"background-color: orange; color: black; {button_style}")
        self.button_back.setFixedSize(250, 40)  
        self.button_back.clicked.connect(self.back)


        layout = QVBoxLayout()
        layout.addWidget(self.label_id)
        layout.addWidget(self.line_edit_id)
        layout.addWidget(self.label_password)
        layout.addWidget(self.line_edit_password)
        layout.addWidget(self.button_enter)
        layout.addWidget(self.button_back)


        layout.setAlignment(Qt.AlignCenter) 

        self.setLayout(layout)

    def back(self) :
        self.page_controller.show_choose_login_page()
    def login(self):
        try:
            entered_id = int(self.line_edit_id.text())
        except ValueError:
            QMessageBox.warning(self, 'Login Status', 'ID must be a number.')
            self.line_edit_id.clear()
            return

        entered_password = self.line_edit_password.text()

        try:
            with db_engine.connect() as connection:
                query = select(customers_table).where(
                    (customers_table.c.c_id == entered_id) & (customers_table.c.c_password == entered_password)
                )
                result = connection.execute(query).fetchall()

                if len(result) > 0:
                    QMessageBox.information(self, 'Login Status', 'Welcome!')
                    self.page_controller.customer_mainpage.customer_id = entered_id
                    self.page_controller.show_customer_main_page()
                else:
                    QMessageBox.warning(self, 'Login Status', 'User not found.')
                    self.line_edit_id.clear()
                    self.line_edit_password.clear()

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))


class PageController:
    def __init__(self):

        self.stacked_widget = QStackedWidget()
        self.choose_login_page = ChooseLoginPage(self)
        self.manager_login_page = ManagerLoginPage(self)
        self.managers_page = ManagersPage(self)
        self.customer_register_page = CustomerRegisterPage(self)
        self.findbookspage = FindBooksPage(None,self)
        self.borrowedbookspage = BorrowedBooks(None,None,None,self)
        self.showbooklist = ShowBooklist(None,None,None,self)
        self.customer_mainpage = CustomerMainPage(None,self)
        self.customer_login_page = CustomerLoginPage(self)
        self.managermainpage = ManagerMainPage(None,self)
        self.editbook = EditBook(None,None, self)
        self.borrowhistory = BorrowHistory(None,self)
        self.findcustomers = FindCustomers(self)
        self.showcustomerslist = ShowCustomerlist( None, self)
        self.addmanager = AddManager(self)
        self.addbook = AddBook(self)
        self.currentborrowers = CurrentBorrowers(self)



        self.stacked_widget.addWidget(self.choose_login_page)
        self.stacked_widget.addWidget(self.manager_login_page)
        self.stacked_widget.addWidget(self.managers_page)
        self.stacked_widget.addWidget(self.customer_register_page)
        self.stacked_widget.addWidget(self.findbookspage)
        self.stacked_widget.addWidget(self.borrowedbookspage)
        self.stacked_widget.addWidget(self.customer_mainpage)
        self.stacked_widget.addWidget(self.showbooklist)
        self.stacked_widget.addWidget(self.customer_login_page)
        self.stacked_widget.addWidget(self.managermainpage)
        self.stacked_widget.addWidget(self.editbook)    
        self.stacked_widget.addWidget(self.borrowhistory)
        self.stacked_widget.addWidget(self.findcustomers)    
        self.stacked_widget.addWidget(self.showcustomerslist)
        self.stacked_widget.addWidget(self.addmanager)
        self.stacked_widget.addWidget(self.addbook)
        self.stacked_widget.addWidget(self.currentborrowers)

        self.stacked_widget.setCurrentIndex(0)


    def show_choose_login_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_manager_login_page(self):
        self.manager_login_page.line_edit_id.clear()
        self.manager_login_page.line_edit_password.clear()
        self.stacked_widget.setCurrentIndex(1)

    def show_managers_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_customer_register_page(self):
        self.customer_register_page.name_input.clear()
        self.customer_register_page.password_input.clear()
        self.customer_register_page.contactinfo_input.clear()
        self.customer_register_page.lastname_input.clear()
        default_date = QDate.fromString("2000-01-01", "yyyy-MM-dd")
        self.customer_register_page.birthdate_input.setDate(default_date)
        self.stacked_widget.setCurrentIndex(3)

    def show_find_books_page(self):
        self.findbookspage.b_name_input.clear()
        self.findbookspage.genre_input.clear()
        self.findbookspage.author_input.clear()
        self.stacked_widget.setCurrentIndex(4)

    def show_borrowed_books_page(self):
        self.stacked_widget.setCurrentIndex(5)

    def show_customer_main_page(self):
        self.stacked_widget.setCurrentIndex(6)

    def show_booklist_page(self):
        self.stacked_widget.setCurrentIndex(7)

    def show_customer_login_page(self):
        self.customer_login_page.line_edit_id.clear()
        self.customer_login_page.line_edit_password.clear()
        self.stacked_widget.setCurrentIndex(8)

    def show_manager_main_page(self):
        self.stacked_widget.setCurrentIndex(9)

    def show_edit_book_page(self):
        self.stacked_widget.setCurrentIndex(10)
    
    def show_borrow_history_page(self):
        self.stacked_widget.setCurrentIndex(11)
    
    def show_find_customers_page(self):
        self.findcustomers.c_id_input.clear()
        self.findcustomers.c_name_input.clear()
        self.findcustomers.c_lastname_input.clear()
        self.findcustomers.c_contactinfo_input.clear()
        self.stacked_widget.setCurrentIndex(12)

    
    def show_customerlist_page(self):
        self.stacked_widget.setCurrentIndex(13)

    def show_add_manager_page(self):
        self.addmanager.name_input.clear()
        self.addmanager.lastname_input.clear()
        self.addmanager.contactinfo_input.clear()
        self.addmanager.password_input.clear()
        self.stacked_widget.setCurrentIndex(14)
    
    def show_add_book_page(self):

        self.addbook.b_name_input.clear()
        self.addbook.genre_input.clear()
        self.addbook.year_input.clear()
        self.addbook.author_input.clear()
        self.addbook.availability_input.clear()
        self.stacked_widget.setCurrentIndex(15)


    def show_current_borrowers_page(self):
        self.stacked_widget.setCurrentIndex(16)

    def get_widget(self):
        return self.stacked_widget

class ManagerMainPage(QWidget):
    def __init__(self, manager_id, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.manager_id = manager_id
        self.init_ui()

        
    def init_ui(self):

        button_style = "QPushButton { background-color: green; color: white; border-radius: 10px; font-size: 18px; }"

        self.button_findbooks = QPushButton("Find Books")
        self.button_findbooks.setFixedSize(400, 100)
        self.button_findbooks.setStyleSheet(button_style)
        self.button_findbooks.clicked.connect(self.find_books)

        self.button_addbook = QPushButton('Add Book')
        self.button_addbook.setFixedSize(400, 100)
        self.button_addbook.setStyleSheet(button_style)
        self.button_addbook.clicked.connect(self.Add_book)

        self.button_findcustomers = QPushButton("Find Customers")
        self.button_findcustomers.setFixedSize(400, 100)
        self.button_findcustomers.setStyleSheet(button_style)
        self.button_findcustomers.clicked.connect(self.find_customers)

        self.button_addmanager = QPushButton("Add Manager")
        self.button_addmanager.setFixedSize(400, 100)
        self.button_addmanager.setStyleSheet(button_style)
        self.button_addmanager.clicked.connect(self.Add_manager)

        self.button_back = QPushButton('Log out')
        self.button_back.setFixedSize(400, 100)
        self.button_back.setStyleSheet('QPushButton { background-color: orange; color: black; border-radius: 10px; font-size: 18px; }')
        self.button_back.clicked.connect(self.back)


        self.layout_choose = QVBoxLayout()
        self.layout_choose.addWidget(self.button_findbooks)
        self.layout_choose.addWidget(self.button_addbook)
        self.layout_choose.addWidget(self.button_findcustomers)
        self.layout_choose.addWidget(self.button_addmanager)
        self.layout_choose.addWidget(self.button_back)

        self.layout_choose.setAlignment(Qt.AlignCenter)

        self.choose_widget = QWidget()
        self.choose_widget.setLayout(self.layout_choose)

        layout = QVBoxLayout()
        layout.addWidget(self.choose_widget)

        self.setLayout(layout)


    def back(self) :
        self.page_controller.show_choose_login_page()
    def find_books(self):
        self.page_controller.findbookspage.forcustomer = False     
        self.page_controller.show_find_books_page()
    def Add_book(self):
        self.page_controller.show_add_book_page()
    def find_customers(self):
        self.page_controller.show_find_customers_page()

    def Add_manager(self):
        self.page_controller.show_add_manager_page()


class AddBook(QWidget):
    def __init__(self, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.init_ui()
    

    def init_ui(self):
    
        self.b_name_input = QLineEdit(self)
        self.genre_input = QLineEdit(self)
        self.year_input = QLineEdit(self)
        self.author_input = QLineEdit(self)
        self.availability_input = QLineEdit(self)

        self.submit_button = QPushButton('Add', self)
        self.submit_button.setFixedSize(500, 50)
        self.submit_button.setStyleSheet("background-color: green; color: white;border-radius: 10px;")
        self.submit_button.clicked.connect(self.addbook)



        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.clicked.connect(self.back)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.button_back)


        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Book Name:'))
        layout.addWidget(self.b_name_input)
        layout.addWidget(QLabel('Genre:'))
        layout.addWidget(self.genre_input)
        layout.addWidget(QLabel('Year Published:'))
        layout.addWidget(self.year_input)
        layout.addWidget(QLabel('Author:'))
        layout.addWidget(self.author_input)
        layout.addWidget(QLabel('Number Available:'))
        layout.addWidget(self.availability_input)


        layout.addLayout(button_layout)


        self.setStyleSheet("""
            QLabel {
                font-size: 26px;
                margin-bottom: 1px;
            }
            QLineEdit, QComboBox, QDateEdit {
                font-size: 26px;
                height: 30px;
            }
            QPushButton {
                font-size: 25px;
                height: 50px;
                background-color: green;
                color: white;  
            }
        """)

    def back(self):
        self.page_controller.show_manager_main_page()
    def addbook(self):

        # Get the input values
        b_name = self.b_name_input.text()
        genre = self.genre_input.text()
        author = self.author_input.text()
        try:
            year = int(self.year_input.text())
            availability = int(self.availability_input.text())
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Year and Availability must be numbers.')
            return        


        if not b_name or not genre or not year or not author or not availability :
            QMessageBox.warning(self, 'Input Error', 'All fields must be filled.')
            return
        

        query = books_table.insert().values(
            b_name = b_name,
            author = author,
            genre = genre,
            p_year = year,
            num_avb = availability
        )

        with db_engine.connect() as connection:
            result = connection.execute(query)
            connection.commit()

        book_id = result.inserted_primary_key[0]

        QMessageBox.information(self, 'Success', f'Book added successfully!\nBook ID is: "{book_id}"')
        self.page_controller.show_manager_main_page()

class AddManager(QWidget):
    def __init__(self, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.init_ui()
    

    def init_ui(self):
    
        self.name_input = QLineEdit(self)
        self.lastname_input = QLineEdit(self)
        self.contactinfo_input = QLineEdit(self)
        self.password_input = QLineEdit(self)

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setFixedSize(500, 50)
        self.submit_button.setStyleSheet("background-color: green; color: white;border-radius: 10px;")
        self.submit_button.clicked.connect(self.submit_registration)



        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.clicked.connect(self.back)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.button_back)


        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Name:'))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel('Last Name:'))
        layout.addWidget(self.lastname_input)
        layout.addWidget(QLabel('Contact Info:'))
        layout.addWidget(self.contactinfo_input)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)


        layout.addLayout(button_layout)


        self.setStyleSheet("""
            QLabel {
                font-size: 26px;
                margin-bottom: 1px;
            }
            QLineEdit, QComboBox, QDateEdit {
                font-size: 26px;
                height: 30px;
            }
            QPushButton {
                font-size: 25px;
                height: 50px;
                background-color: green;
                color: white;  
            }
        """)

    def back(self):
        self.page_controller.show_manager_main_page()
    def submit_registration(self):

        # Get the input values
        name = self.name_input.text()
        lastname = self.lastname_input.text()
        contactinfo = self.contactinfo_input.text()
        password = self.password_input.text()
        


        if not name or not lastname or not contactinfo or not password:
            QMessageBox.warning(self, 'Input Error', 'All fields must be filled.')
            return
      

        query = managers_table.insert().values(
            m_name=name,
            m_lastname=lastname,
            m_contactinfo=contactinfo,
            m_password=password,
            
        )

        with db_engine.connect() as connection:
            result = connection.execute(query)
            connection.commit()

        manager_id = result.inserted_primary_key[0]

        QMessageBox.information(self, 'Success', f'Manager added successfully!\nManager ID is: "{manager_id}"')
        self.page_controller.show_manager_main_page()

class FindCustomers(QWidget):
    def __init__(self, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.init_ui()

    def init_ui(self):

        self.c_id_input = QLineEdit(self)
        self.c_name_input = QLineEdit(self)
        self.c_lastname_input = QLineEdit(self)
        self.c_contactinfo_input = QLineEdit(self)
        self.c_gender_input = QComboBox(self)
        self.c_gender_input.addItems([ 'All', 'Male', 'Female'])
        self.birthdate_before_input = QDateEdit(self)
        self.birthdate_after_input = QDateEdit(self)
        self.birthdate_before_input.setDisplayFormat("yyyy-MM-dd")
        self.birthdate_after_input.setDisplayFormat("yyyy-MM-dd")

        self.submit_button = QPushButton('Search', self)
        self.submit_button.setFixedSize(500, 50)
        self.submit_button.setStyleSheet("background-color: green; color: white;border-radius: 10px;")
        self.submit_button.clicked.connect(self.submit_search)

        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.clicked.connect(self.back)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.button_back)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Customer ID:'))
        layout.addWidget(self.c_id_input)
        layout.addWidget(QLabel('Customer Name:'))
        layout.addWidget(self.c_name_input)
        layout.addWidget(QLabel('Customer Lastname:'))
        layout.addWidget(self.c_lastname_input)
        layout.addWidget(QLabel('Contact Information:'))
        layout.addWidget(self.c_contactinfo_input)
        layout.addWidget(QLabel('Gender:'))
        layout.addWidget(self.c_gender_input)
        layout.addWidget(QLabel('Birthday Before:'))
        layout.addWidget(self.birthdate_before_input)
        layout.addWidget(QLabel('Birthday After:'))
        layout.addWidget(self.birthdate_after_input)


        layout.addLayout(button_layout)


        self.setStyleSheet("""
            QLabel {
                font-size: 26px;
                margin-bottom: 1px;
            }
            QLineEdit, QComboBox, QDateEdit {
                font-size: 26px;
                height: 30px;
            }
            QPushButton {
                font-size: 25px;
                height: 50px;
                background-color: green;
                color: white;  
            }
        """)

    def back(self):
        self.page_controller.show_manager_main_page()
    def submit_search(self):
        # Get the input values
        c_id_text = self.c_id_input.text()
        c_name = self.c_name_input.text()
        c_lastname = self.c_lastname_input.text()
        c_contactinfo = self.c_contactinfo_input.text()
        c_gender = self.c_gender_input.currentText()
        c_birthdate_before = self.birthdate_before_input.date().toString("yyyy-MM-dd")
        c_birthdate_after = self.birthdate_after_input.date().toString("yyyy-MM-dd")

        query = select(customers_table).where(                
            (customers_table.c.c_name.like(f'%{c_name}%')) &
            (customers_table.c.c_lastname.like(f'%{c_lastname}%')) &
            (customers_table.c.c_contactinfo.like(f'%{c_contactinfo}%')) &
            (customers_table.c.c_birthdate.between(c_birthdate_after, c_birthdate_before))
        )
        if c_id_text:
            try:
                c_id = int(c_id_text)
            except ValueError:
                QMessageBox.warning(self,'Input Error', 'ID must be a number.')
                return  
            query = query.where(customers_table.c.c_id == c_id)

        if c_gender != "All":
            query = query.where(customers_table.c.c_gender == c_gender)

        with db_engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()
            connection.commit()

        # Check if any customers were found
        if len(rows) == 0:
            QMessageBox.warning(self, 'No Customers Found', 'No customers were found that match your search criteria.')
        else:
            # If customers were found, go to the Showcustomerlist page and display the results
            self.page_controller.showcustomerslist.result = rows
            self.page_controller.showcustomerslist.load_data()
            self.page_controller.show_customerlist_page()
            
class ShowCustomerlist(QWidget):
    def __init__(self, result, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.result = result
        self.init_ui()

    def init_ui(self):

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.setFont(QFont("Arial", 18))
        self.button_back.clicked.connect(self.back)

        layout = QGridLayout()
        layout.addWidget(self.table, 0, 0)  
        layout.addWidget(self.button_back, 1, 0, alignment=Qt.AlignCenter)

        layout.setRowStretch(0, 1) 
        layout.setRowStretch(1, 0)  

        self.setLayout(layout)
        
    def back(self):
        self.page_controller.show_find_customers_page()
    def load_data(self):
        self.table.setSortingEnabled(False)
        self.table.clear()
        custom_column_names = ['ID', 'Name', 'Lastname', 'Contact info', 'Password', 'gender', 'Birthdate' , 'Action']
        
        self.table.setColumnCount(len(custom_column_names))
        self.table.setRowCount(len(self.result))
        self.table.setHorizontalHeaderLabels(custom_column_names)

        font = QFont()
        font.setPointSize(15)

        fonth = QFont()
        fonth.setPointSize(15) 
        fonth.setBold(True)

        self.table.horizontalHeader().setFont(fonth)

        for i, row in enumerate(self.result):
            for j, value in enumerate(row):
                if j == 0:  # columns with integer values
                    item = IntegerTableWidgetItem(str(value))
                else:
                    item = QTableWidgetItem(str(value))
                item.setFont(font)  
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

            boooks_button = QPushButton('Books')
            boooks_button.setFont(font)  
            boooks_button.setStyleSheet("background-color: green; color: white; border-radius: 20px; padding: 10px; font-size: 16px; border: 2px black;")
            boooks_button.clicked.connect(self.customer_books)
            self.table.setCellWidget(i, 7, boooks_button)

        # Set the height of each row
        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i, 60)

        # Set the width of each column
        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, 231)

        self.table.setSortingEnabled(True)
    
    def customer_books(self):

        button = self.sender()
        index = self.table.indexAt(button.pos())
        row = index.row()
        customer_id = int(self.table.item(row, 0).text())
        self.page_controller.borrowhistory.customer_id = customer_id
        self.page_controller.borrowhistory.for_customer = False
        self.page_controller.borrowhistory.load_data()

class ChooseLoginPage(QWidget):
    
    def __init__(self, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.init_ui()

    def init_ui(self):
        

        button_style = "QPushButton { background-color: green; color: white; border-radius: 10px; font-size: 18px; }"

        self.button_manager = QPushButton('Login Manager')
        self.button_manager.setFixedSize(400, 100)
        self.button_manager.setStyleSheet(button_style)
        self.button_manager.clicked.connect(self.login_manager)
        



        self.button_customer = QPushButton('Login Customer')
        self.button_customer.setFixedSize(400, 100)
        self.button_customer.setStyleSheet(button_style)
        self.button_customer.clicked.connect(self.login_customer)

        self.button_register = QPushButton('Register')
        self.button_register.setFixedSize(400, 100)
        self.button_register.setStyleSheet(button_style)
        self.button_register.clicked.connect(self.register_customer)


        self.layout_choose = QVBoxLayout()
        self.layout_choose.addWidget(self.button_manager)
        self.layout_choose.addWidget(self.button_customer)
        self.layout_choose.addWidget(self.button_register)

        self.layout_choose.setAlignment(Qt.AlignCenter)

        self.choose_widget = QWidget()
        self.choose_widget.setLayout(self.layout_choose)

        layout = QVBoxLayout()
        layout.addWidget(self.choose_widget)
        self.setLayout(layout)

    def login_manager(self):
        self.page_controller.show_manager_login_page()

    def login_customer(self):
        self.page_controller.show_customer_login_page()

    def register_customer(self):
        self.page_controller.show_customer_register_page()

class CustomerMainPage(QWidget):
    def __init__(self, customer_id, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.customer_id = customer_id
        self.init_ui()

        
    def init_ui(self):

        button_style = "QPushButton { background-color: green; color: white; border-radius: 10px; font-size: 18px; }"

        self.button_findbooks = QPushButton("Find Books")
        self.button_findbooks.setFixedSize(400, 100)
        self.button_findbooks.setStyleSheet(button_style)
        self.button_findbooks.clicked.connect(self.find_books)

        self.button_borrowedbooks = QPushButton('Borrowd Books')
        self.button_borrowedbooks.setFixedSize(400, 100)
        self.button_borrowedbooks.setStyleSheet(button_style)
        self.button_borrowedbooks.clicked.connect(self.find_borrowed_books)

        self.button_borrowhistory = QPushButton('Borrow History')
        self.button_borrowhistory.setFixedSize(400, 100)
        self.button_borrowhistory.setStyleSheet(button_style)
        self.button_borrowhistory.clicked.connect(self.borrowe_history)

        self.button_back = QPushButton('Log out')
        self.button_back.setFixedSize(400, 100)
        self.button_back.setStyleSheet('QPushButton { background-color: orange; color: black; border-radius: 10px; font-size: 18px; }')
        self.button_back.clicked.connect(self.back)


        self.layout_choose = QVBoxLayout()
        self.layout_choose.addWidget(self.button_findbooks)
        self.layout_choose.addWidget(self.button_borrowedbooks)
        self.layout_choose.addWidget(self.button_borrowhistory)
        self.layout_choose.addWidget(self.button_back)

        self.layout_choose.setAlignment(Qt.AlignCenter)

        self.choose_widget = QWidget()
        self.choose_widget.setLayout(self.layout_choose)


        layout = QVBoxLayout()
        layout.addWidget(self.choose_widget)

        self.setLayout(layout)

    def borrowe_history(self):

        self.page_controller.borrowhistory.customer_id = self.customer_id
        self.page_controller.borrowhistory.load_data()

    def back(self) :
        self.page_controller.show_choose_login_page()
    def find_books(self):
        self.page_controller.findbookspage.customer_id = self.customer_id 
        self.page_controller.findbookspage.forcustomer = True      
        self.page_controller.show_find_books_page()
        
    def find_borrowed_books(self):
        # Join the tables and select the columns
        query = (
            select(
                books_table.c.b_id,
                books_table.c.b_name,
                books_table.c.author,
                books_table.c.genre,
                books_table.c.p_year,
                customers_books_table.c.Borrow_Date
            )
            .join_from(customers_books_table, books_table, customers_books_table.c.b_id == books_table.c.b_id)
            .where(customers_books_table.c.c_id == self.customer_id)
        )

        with db_engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

        if len(rows) == 0:
            QMessageBox.warning(self, 'No Books Found', 'You do not currently have a borrowed book')
            self.page_controller.show_customer_main_page()
        else:
            # If books were found, go to the BorrowedBooks page and display the results
            self.page_controller.borrowedbookspage.result = rows
            self.page_controller.borrowedbookspage.find_borrowed_books = self
            self.page_controller.borrowedbookspage.customer_id = self.customer_id
            self.page_controller.borrowedbookspage.load_data()
            self.page_controller.show_borrowed_books_page()
        
class BorrowedBooks(QWidget):
    
     def __init__(self, result, customer_id, find_borrowed_books, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.customer_id = customer_id
        self.find_borrowed_books = find_borrowed_books
        self.result = result
        self.init_ui()

     def init_ui(self):

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.setFont(QFont("Arial", 18))
        self.button_back.clicked.connect(self.back)

        layout = QGridLayout()
        layout.addWidget(self.table, 0, 0)  
        layout.addWidget(self.button_back, 1, 0, alignment=Qt.AlignCenter)

        layout.setRowStretch(0, 1) 
        layout.setRowStretch(1, 0)  

        self.setLayout(layout)

     def back(self):
        self.page_controller.show_customer_main_page()
     def load_data(self):

        self.table.setSortingEnabled(False)
        self.table.clear()
        custom_column_names = ['ID', 'Name', 'Author', 'Genre', 'Year', 'Date Borrowed' , 'Return'] 
        
        self.table.setColumnCount(len(custom_column_names))
        self.table.setRowCount(len(self.result))
        self.table.setHorizontalHeaderLabels(custom_column_names)
       
        font = QFont()
        font.setPointSize(15) 
        fonth = QFont()
        fonth.setPointSize(15) 
        fonth.setBold(True)  

        self.table.horizontalHeader().setFont(fonth)


        for i, row in enumerate(self.result):
            for j, value in enumerate(row):
                if j in [0, 4]:  # columns with integer values
                    item = IntegerTableWidgetItem(str(value))
                else:
                    item = QTableWidgetItem(str(value))
                item.setFont(font)  
                item.setTextAlignment(Qt.AlignCenter)  
                self.table.setItem(i, j, item)
            return_button = QPushButton('Return')
            return_button.setFont(font)  
            return_button.setStyleSheet("background-color: green; color: white; border-radius: 20px; padding: 10px; font-size: 16px; border: 2px black;")
            return_button.clicked.connect(self.return_book)
            self.table.setCellWidget(i, 6, return_button)

        # Set the height of each row
        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i, 60)

        # Set the width of each column
        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, 265)

        self.table.setSortingEnabled(True)
     def return_book(self):
        # Find out which row the button is in
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row = index.row()

        book_id = int(self.table.item(row, 0).text()) 
        book_name = self.table.item(row,1).text()
        return_date = date.today()

        with db_engine.connect() as connection:

            # update customers_books_history table 
            query = update(customers_books_history_table).where(
            customers_books_history_table.c.b_id == book_id,
            customers_books_history_table.c.c_id == self.customer_id,
            customers_books_history_table.c.date_returned == '9999-12-31'
            ).values(
                date_returned = date.today()
            )
            connection.execute(query)

            # update the book's availablity
            query = update(books_table).where(books_table.c.b_id == book_id).values(num_avb = books_table.c.num_avb + 1)
            connection.execute(query)
           
            # remove item from customers_books table
            query = delete(customers_books_table).where(
            customers_books_table.c.b_id == book_id,
            customers_books_table.c.c_id == self.customer_id
            )

            connection.execute(query)

            connection.commit()


        QMessageBox.information(self, 'Book Returend', f'book {book_id}, "{book_name}" Returned Successfully.')
        self.find_borrowed_books.find_borrowed_books()

class BorrowHistory(QWidget):
     def __init__(self,customer_id, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.customer_id = customer_id
        self.for_customer = True
        self.init_ui()

     def init_ui(self):

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.setFont(QFont("Arial", 18))
        self.button_back.clicked.connect(self.back)

        layout = QGridLayout()
        layout.addWidget(self.table, 0, 0)  
        layout.addWidget(self.button_back, 1, 0, alignment=Qt.AlignCenter)

        layout.setRowStretch(0, 1) 
        layout.setRowStretch(1, 0)  

        self.setLayout(layout)



     def back(self):
        if(self.for_customer):
            self.page_controller.show_customer_main_page()
        else:
            self.for_customer = True
            self.page_controller.show_customerlist_page()
     def load_data(self):
        self.table.setSortingEnabled(False)
        self.table.clear()

        query = (
            select(
                books_table.c.b_id,
                books_table.c.b_name,
                books_table.c.author,
                books_table.c.genre,
                books_table.c.p_year,
                customers_books_history_table.c.date_borrowed,
                customers_books_history_table.c.date_returned
            )
            .join_from(customers_books_history_table, books_table, customers_books_history_table.c.b_id == books_table.c.b_id)
            .where(customers_books_history_table.c.c_id == self.customer_id)
        )

        with db_engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

        if len(rows) == 0:
            QMessageBox.warning(self, 'No Books Found', 'No books have been borrowed yet')
            if(self.for_customer):
                self.page_controller.show_customer_main_page()
            else:
                self.for_customer = True
                self.page_controller.show_customerlist_page()
        else:


            custom_column_names = ['Book ID','Book Name', 'Author', 'Genre', 'Year', 'Borrow Date', 'Return Date']

            self.table.setColumnCount(len(custom_column_names))
            self.table.setRowCount(len(rows))
            self.table.setHorizontalHeaderLabels(custom_column_names)

            font = QFont()
            font.setPointSize(15) 

            fonth = QFont()
            fonth.setPointSize(15) 
            fonth.setBold(True) 

            self.table.horizontalHeader().setFont(fonth)


            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    if j in [0, 4]:
                        item = IntegerTableWidgetItem(str(value))
                    elif j==6:
                        if str(value).startswith('9999'):
                            item = QTableWidgetItem('Not yet returned')
                        else: item = QTableWidgetItem(str(value))
                    else:
                        item = QTableWidgetItem(str(value))
                    item.setFont(font) 
                    item.setTextAlignment(Qt.AlignCenter) 
                    self.table.setItem(i, j, item)




            # Set the height of each row
            for i in range(self.table.rowCount()):
                self.table.setRowHeight(i, 60)

            # Set the width of each column
            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, 270)

            self.table.setSortingEnabled(True)   
            self.page_controller.show_borrow_history_page()

class FindBooksPage(QWidget):
    def __init__(self, customer_id, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.customer_id = customer_id
        self.forcustomer = True

        self.init_ui()

    def init_ui(self):

        self.b_name_input = QLineEdit(self)
        self.genre_input = QLineEdit(self)
        self.before_year_input = QLineEdit(self)
        self.after_year_input = QLineEdit(self)
        self.author_input = QLineEdit(self)
        self.availability_input = QComboBox(self)
        self.availability_input.addItems(['Available to borrow', 'All'])
        self.before_year_input.setText('2024')
        self.after_year_input.setText('1')


        self.submit_button = QPushButton('Search', self)
        self.submit_button.setFixedSize(500, 50)  
        self.submit_button.setStyleSheet("background-color: green; color: white;border-radius: 10px;")
        self.submit_button.clicked.connect(self.submit_search)

        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.clicked.connect(self.back)

        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.button_back)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Book Name:'))
        layout.addWidget(self.b_name_input)
        layout.addWidget(QLabel('Genre:'))
        layout.addWidget(self.genre_input)
        layout.addWidget(QLabel('Before Year:'))
        layout.addWidget(self.before_year_input)
        layout.addWidget(QLabel('After Year:'))
        layout.addWidget(self.after_year_input)
        layout.addWidget(QLabel('Author:'))
        layout.addWidget(self.author_input)
        layout.addWidget(QLabel('Availability:'))
        layout.addWidget(self.availability_input)


        layout.addLayout(button_layout)


        self.setStyleSheet("""
            QLabel {
                font-size: 26px;
                margin-bottom: 1px;
            }
            QLineEdit, QComboBox, QDateEdit {
                font-size: 26px;
                height: 30px;
            }
            QPushButton {
                font-size: 25px;
                height: 50px;
                background-color: green;
                color: white;  
            }
        """)
    def back(self):
        if(self.forcustomer):
            self.page_controller.show_customer_main_page()
        else:
            self.page_controller.show_manager_main_page()
    def submit_search(self):
        # Get the input values
        b_name = self.b_name_input.text()
        genre = self.genre_input.text()
        before_year = self.before_year_input.text()
        if (not before_year):
            before_year = 2024
        after_year = self.after_year_input.text()
        if (not after_year):
            after_year = 1
        author = self.author_input.text()
        availability = self.availability_input.currentText()
        query = select(books_table).where(
            (books_table.c.b_name.like(f'%{b_name}%')) &
            (books_table.c.genre.like(f'%{genre}%')) &
            (books_table.c.p_year <= int(before_year)) &
            (books_table.c.p_year >= int(after_year)) &
            (books_table.c.author.like(f'%{author}%')) &
            (
                (books_table.c.num_avb > 1)
                if availability == 'Available to borrow'
                else True
            )
        )
        with db_engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()
            connection.commit()

        # Check if any books were found
        if len(rows) == 0:
            QMessageBox.warning(self, 'No Books Found', 'No books were found that match your search criteria.')
        else:
            if(self.forcustomer):
                # If books were found, go to the ShowBooklist page and display the results
                self.page_controller.showbooklist.result = rows
                self.page_controller.showbooklist.forcustomer = True
                self.page_controller.showbooklist.find_books_page = self
                self.page_controller.showbooklist.customer_id = self.customer_id
                self.page_controller.showbooklist.load_data()
                self.page_controller.show_booklist_page()
            else:
                self.page_controller.showbooklist.result = rows
                self.page_controller.showbooklist.forcustomer = False
                self.page_controller.showbooklist.find_books_page = self
                self.page_controller.showbooklist.load_data()
                self.page_controller.show_booklist_page()

class ShowBooklist(QWidget):
    def __init__(self, result, customer_id, find_books_page, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.customer_id = customer_id
        self.find_books_page = find_books_page
        self.forcustomer = True
        self.result = result
        self.init_ui()

    def init_ui(self):

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.setFont(QFont("Arial", 18))
        self.button_back.clicked.connect(self.back)

        layout = QGridLayout()
        layout.addWidget(self.table, 0, 0)  
        layout.addWidget(self.button_back, 1, 0, alignment=Qt.AlignCenter)

        layout.setRowStretch(0, 1) 
        layout.setRowStretch(1, 0)  

        self.setLayout(layout)
 
    def back(self):
        self.page_controller.show_find_books_page()
    
    def load_data(self):
        self.table.setSortingEnabled(False)
        self.table.clear()

        if(self.forcustomer):
            custom_column_names = ['ID', 'Name', 'Author', 'Genre', 'Year', 'Availability', 'Action']
            
            self.table.setColumnCount(len(custom_column_names))
            self.table.setRowCount(len(self.result))
            self.table.setHorizontalHeaderLabels(custom_column_names)
            
            font = QFont()
            font.setPointSize(15)  

            fonth = QFont()
            fonth.setPointSize(15) 
            fonth.setBold(True)

            self.table.horizontalHeader().setFont(fonth)


            for i, row in enumerate(self.result):
                for j, value in enumerate(row):
                    if j in [0, 4, 5]:  # columns with integer values
                        item = IntegerTableWidgetItem(str(value))
                    else:
                        item = QTableWidgetItem(str(value))
                    item.setFont(font)  
                    item.setTextAlignment(Qt.AlignCenter)  
                    self.table.setItem(i, j, item)
                borrow_button = QPushButton('Borrow')
                borrow_button.setFont(font)  
                borrow_button.setStyleSheet("background-color: green; color: white; border-radius: 20px; padding: 10px; font-size: 16px; border: 2px black;")
                borrow_button.clicked.connect(self.borrow_book)
                self.table.setCellWidget(i, 6, borrow_button)
                
            # Set the height of each row
            for i in range(self.table.rowCount()):
                self.table.setRowHeight(i, 60)

            # Set the width of each column
            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, 265)

            self.table.setSortingEnabled(True)  

        else:
            custom_column_names = ['ID', 'Name', 'Author', 'Genre', 'Year', 'Availability', 'Edit', 'Current Borrowers']
            
            self.table.setColumnCount(len(custom_column_names))
            self.table.setRowCount(len(self.result))
            self.table.setHorizontalHeaderLabels(custom_column_names)
           
            font = QFont()
            font.setPointSize(15)  

            fonth = QFont()
            fonth.setPointSize(15) 
            fonth.setBold(True)

            self.table.horizontalHeader().setFont(fonth)


            for i, row in enumerate(self.result):
                for j, value in enumerate(row):
                    if j in [0, 4, 5]:  # columns with integer values
                        item = IntegerTableWidgetItem(str(value))
                    else:
                        item = QTableWidgetItem(str(value))
                    item.setFont(font)  
                    item.setTextAlignment(Qt.AlignCenter) 
                    self.table.setItem(i, j, item)
                
                edit_button = QPushButton('Edit')
                edit_button.setFont(font)  
                edit_button.setStyleSheet("background-color: green; color: white; border-radius: 20px; padding: 10px; font-size: 16px; border: 2px black;")
                edit_button.clicked.connect(self.edit_book)
                self.table.setCellWidget(i, 6, edit_button)

                seeborrowers_button = QPushButton('Current Borrowers')
                seeborrowers_button.setFont(font)  
                seeborrowers_button.setStyleSheet("background-color: green; color: white; border-radius: 20px; padding: 10px; font-size: 16px; border: 2px black;")
                seeborrowers_button.clicked.connect(self.current_borrowers)
                self.table.setCellWidget(i, 7, seeborrowers_button)

            # Set the height of each row
            for i in range(self.table.rowCount()):
                self.table.setRowHeight(i, 60)

            # Set the width of each column
            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, 230)

            self.table.setSortingEnabled(True) 
    
    def current_borrowers(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row = index.row()
        book_id = int(self.table.item(row, 0).text())
        self.page_controller.currentborrowers.book_id = book_id
        self.page_controller.currentborrowers.load_data()

    def edit_book(self):

        button = self.sender()
        index = self.table.indexAt(button.pos())
        row = index.row()
        book_id = int(self.table.item(row, 0).text())

        self.page_controller.editbook.book_id = book_id
        self.page_controller.editbook.find_books_page = self.find_books_page
        self.page_controller.editbook.editbook()
        self.page_controller.show_edit_book_page()

    def borrow_book(self):
        # Find out which row the button is in
        button = self.sender()
        index = self.table.indexAt(button.pos())
        row = index.row()

        book_id = int(self.table.item(row, 0).text())
        book_name = self.table.item(row,1).text()

        with db_engine.connect() as connection:

            # Check the availability of the book
            query = select(books_table.c.num_avb).where(books_table.c.b_id == book_id)

            num_avb_item = self.table.item(row, 5)
            num_avb = int(num_avb_item.text())

            if num_avb <= 1:
                QMessageBox.warning(self, 'Book Unavailable', f'This is the last available stock of book {book_id}, "{book_name}". Can not be borrowed.')
                return
            query = select(customers_books_table.c).where(
                (customers_books_table.c.c_id == self.customer_id) &
                (customers_books_table.c.b_id == book_id)
            )
            result = connection.execute(query)
            row = result.fetchone()
            if row is not None:
                QMessageBox.warning(self, 'Book Already Borrowed', f'You have already borrowed one copy of book {book_id}, "{book_name}".')
                return

            # Check if the book has already been borrowed by the customer on the same day
            query = select(customers_books_history_table.c).where(
                (customers_books_history_table.c.c_id == self.customer_id) &
                (customers_books_history_table.c.b_id == book_id) &
                (customers_books_history_table.c.date_borrowed == date.today())
            )
            result = connection.execute(query)
            row = result.fetchone()
            if row is not None:
                QMessageBox.warning(self, 'Book Already Borrowed Today and then returned, ', f'You have already borrowed book {book_id}, "{book_name}" today and returned it.')
                return


        

            # Insert the customer_id and book_id into the customers_books table
            query = customers_books_table.insert().values(
                c_id=self.customer_id,
                b_id=book_id,
                Borrow_Date=date.today()
            )
            connection.execute(query)

            #  Insert the customer_id and book_id into the customers_books_history table
            query = customers_books_history_table.insert().values(
                c_id=self.customer_id,
                b_id=book_id,
                date_borrowed = date.today()
            )
            connection.execute(query)
            # update the book's availablity
            query = (
                update(books_table).
                where(books_table.c.b_id == book_id).
                values(num_avb=books_table.c.num_avb - 1)
            )
            connection.execute(query)
            connection.commit()


        self.find_books_page.submit_search()
        QMessageBox.information(self, 'Book Borrowed', f'Customer {self.customer_id} borrowed book {book_id}, "{book_name}".')



class EditBook(QWidget):
    def __init__(self,book_id,find_books_page, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.book_id = book_id
        self.find_books_page = find_books_page
        self.init_ui() 

    def init_ui(self):

        


        self.b_name_input = QLineEdit(self)
        self.genre_input = QLineEdit(self)
        self.year_published_input = QLineEdit(self)
        self.author_input = QLineEdit(self)
        self.availability_input = QLineEdit(self)

        self.submit_button = QPushButton('Apply', self)
        self.submit_button.setFixedSize(500, 50)
        self.submit_button.setStyleSheet("background-color: green; color: white;border-radius: 10px;")
        self.submit_button.clicked.connect(self.applychanges)

        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.clicked.connect(self.back)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.button_back)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Book Name:'))
        layout.addWidget(self.b_name_input)
        layout.addWidget(QLabel('Genre:'))
        layout.addWidget(self.genre_input)
        layout.addWidget(QLabel('Year Published:'))
        layout.addWidget(self.year_published_input)
        layout.addWidget(QLabel('Author:'))
        layout.addWidget(self.author_input)
        layout.addWidget(QLabel('Availability:'))
        layout.addWidget(self.availability_input)


        layout.addLayout(button_layout)


        self.setStyleSheet("""
            QLabel {
                font-size: 26px;
                margin-bottom: 1px;
            }
            QLineEdit, QComboBox, QDateEdit {
                font-size: 26px;
                height: 30px;
            }
            QPushButton {
                font-size: 25px;
                height: 50px;
                background-color: green;
                color: white;  
            }
        """)
    
    def editbook(self):

        query = select(
            books_table.c.b_name,
            books_table.c.p_year,
            books_table.c.genre,
            books_table.c.author,
            books_table.c.num_avb
        ).where(
            books_table.c.b_id == self.book_id
        )

        with db_engine.connect() as connection:
            result = connection.execute(query)
            book_info = result.fetchone()
            connection.commit()

        b_name, p_year, genre, author, num_avb = book_info
        

        self.b_name_input.setText(b_name)
        self.genre_input.setText(genre)
        self.year_published_input.setText(str(p_year))
        self.author_input.setText(author)
        self.availability_input.setText(str(num_avb))

    def back(self):
        self.page_controller.show_booklist_page()

    def applychanges(self):
        b_name = self.b_name_input.text()
        genre = self.genre_input.text()
        author = self.author_input.text()
        

        try:
            p_year = int(self.year_published_input.text())
            num_avb = int(self.availability_input.text())
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Year and Availability must be numbers.')
            return        


        if not b_name or not genre or not p_year or not author or not num_avb :
            QMessageBox.warning(self, 'Input Error', 'All fields must be filled.')
            return

        update_stmt = update(books_table).where(books_table.c.b_id == self.book_id).values(
            b_name=b_name,
            genre=genre,
            p_year=p_year,
            author=author,
            num_avb=num_avb
        )

        with db_engine.connect() as connection:
            result = connection.execute(update_stmt)
            connection.commit()


        QMessageBox.information(self, 'Book Edited', f'Data changed for book {self.book_id}, "{b_name}".')
        self.find_books_page.submit_search()

class CurrentBorrowers(QWidget):
    def __init__(self, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.book_id = None
        self.init_ui()

    def init_ui(self):

        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.setFont(QFont("Arial", 18))
        self.button_back.clicked.connect(self.back)

        layout = QGridLayout()
        layout.addWidget(self.table, 0, 0)  
        layout.addWidget(self.button_back, 1, 0, alignment=Qt.AlignCenter)

        layout.setRowStretch(0, 1) 
        layout.setRowStretch(1, 0)  

        self.setLayout(layout)

    def back(self):
        self.page_controller.show_booklist_page()

    def load_data(self):
        self.table.setSortingEnabled(False)
        self.table.clear()

        query = (
            select(
                customers_table.c.c_id,
                customers_table.c.c_name,
                customers_table.c.c_lastname,
                customers_table.c.c_contactinfo,
                customers_table.c.c_gender,
                customers_books_table.c.Borrow_Date,
            )
            .join_from(customers_books_table, customers_table, customers_books_table.c.c_id == customers_table.c.c_id)
            .where(customers_books_table.c.b_id == self.book_id)
        )

        with db_engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

        if len(rows) == 0:
            QMessageBox.warning(self, 'No current borrowers', 'This books has no current borrowers')
            self.page_controller.show_booklist_page()
            
        else:


            custom_column_names = ['Customer ID','Customer Name', 'Customer lastname', 'Contact info', 'Gender', 'Borrow Date']

            self.table.setColumnCount(len(custom_column_names))
            self.table.setRowCount(len(rows))
            self.table.setHorizontalHeaderLabels(custom_column_names)
            
            font = QFont()
            font.setPointSize(15) 

            fonth = QFont()
            fonth.setPointSize(15) 
            fonth.setBold(True) 

            self.table.horizontalHeader().setFont(fonth)


            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    if j== 0:
                        item = IntegerTableWidgetItem(str(value))
                    else:
                        item = QTableWidgetItem(str(value))
                    item.setFont(font)   
                    item.setTextAlignment(Qt.AlignCenter) 
                    self.table.setItem(i, j, item)




            # Set the height of each row
            for i in range(self.table.rowCount()):
                self.table.setRowHeight(i, 60)

            # Set the width of each column
            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, 310)

            self.table.setSortingEnabled(True)  
            self.page_controller.show_current_borrowers_page()

            
class ManagersPage(QWidget):
    def __init__(self, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.init_ui()

    def init_ui(self):



        self.table = QTableWidget()
        self.load_data()

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_data(self):
        with db_engine.connect() as connection:
            query = select(managers_table)
            result = connection.execute(query).fetchall()

            if result:
                custom_column_names = ['ID', 'Name', 'Last Name', 'Phone Number', 'Password']  

                self.table.setColumnCount(len(custom_column_names))
                self.table.setRowCount(len(result))
                self.table.setHorizontalHeaderLabels(custom_column_names)

                for i, row in enumerate(result):
                    for j, value in enumerate(row):
                        self.table.setItem(i, j, QTableWidgetItem(str(value)))
            else:
                QMessageBox.warning(self, 'No Data', 'No managers found.')

class CustomerRegisterPage(QWidget):
    def __init__(self, page_controller):
        super().__init__()
        self.page_controller = page_controller
        self.init_ui()
    

    def init_ui(self):
    
        self.name_input = QLineEdit(self)
        self.lastname_input = QLineEdit(self)
        self.contactinfo_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.gender_input = QComboBox(self)
        self.gender_input.addItems(['Male', 'Female'])
        self.birthdate_input = QDateEdit(self)
        self.birthdate_input.setDisplayFormat("yyyy-MM-dd")

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setFixedSize(500, 50)
        self.submit_button.setStyleSheet("background-color: green; color: white;border-radius: 10px;")
        self.submit_button.clicked.connect(self.submit_registration)



        self.button_back = QPushButton('Back')
        self.button_back.setFixedSize(500, 50)
        self.button_back.setStyleSheet("background-color: orange; color: black;border-radius: 10px;")
        self.button_back.clicked.connect(self.back)

        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.button_back)


        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Name:'))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel('Last Name:'))
        layout.addWidget(self.lastname_input)
        layout.addWidget(QLabel('Contact Info:'))
        layout.addWidget(self.contactinfo_input)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel('Gender:'))
        layout.addWidget(self.gender_input)
        layout.addWidget(QLabel('Birthdate:'))
        layout.addWidget(self.birthdate_input)

        layout.addLayout(button_layout)


        self.setStyleSheet("""
            QLabel {
                font-size: 26px;
                margin-bottom: 1px;
            }
            QLineEdit, QComboBox, QDateEdit {
                font-size: 26px;
                height: 30px;
            }
            QPushButton {
                font-size: 25px;
                height: 50px;
                background-color: green;
                color: white;  
            }
        """)

    def back(self):
        self.page_controller.show_choose_login_page()
    def submit_registration(self):

        # Get the input values
        name = self.name_input.text()
        lastname = self.lastname_input.text()
        contactinfo = self.contactinfo_input.text()
        password = self.password_input.text()
        gender = self.gender_input.currentText()
        birthdate = self.birthdate_input.date()


        if not name or not lastname or not contactinfo or not password or not gender:
            QMessageBox.warning(self, 'Input Error', 'All fields must be filled.')
            return
        if birthdate.year() >= 2004:
            QMessageBox.warning(self, 'Input Error', 'Birthdate must be before 2004.')
            return
        birthdate = self.birthdate_input.date().toString("yyyy-MM-dd")

        query = customers_table.insert().values(
            c_name=name,
            c_lastname=lastname,
            c_contactinfo=contactinfo,
            c_password=password,
            c_gender=gender,
            c_birthdate=birthdate
        )

        with db_engine.connect() as connection:
            result = connection.execute(query)
            connection.commit()

        customer_id = result.inserted_primary_key[0]

       
        QMessageBox.information(self, 'Success', f'Customer registered successfully!\nYour ID is: "{customer_id}"')
        self.page_controller.customer_mainpage.customer_id = customer_id
        self.page_controller.show_customer_main_page()
       
def main():
    app = QApplication(sys.argv)



    app.setStyle('Fusion')

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(116, 215, 112))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(palette)
    
    page_controller = PageController()
    page_controller.get_widget().show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
