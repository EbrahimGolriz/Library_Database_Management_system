CREATE TABLE books (
    b_id INT IDENTITY(1,1) PRIMARY KEY,
    b_name VARCHAR(100),
    author VARCHAR(100),
    genre VARCHAR(50),
    p_year INT,
    num_avb INT
);

CREATE TABLE managers (
    m_id INT IDENTITY(1,1) PRIMARY KEY,
    m_name VARCHAR(100),
    m_lastname VARCHAR(100),
    m_contactinfo VARCHAR(100),
    m_password VARCHAR(50)
);


CREATE TABLE customers (
    c_id INT IDENTITY(1,1) PRIMARY KEY,
    c_name VARCHAR(100),
    c_lastname VARCHAR(100),
    c_contactinfo VARCHAR(100),
    c_password VARCHAR(50),
    c_gender VARCHAR(10),
    c_birthdate DATE
);


CREATE TABLE customers_books (
    c_id INT,
    b_id INT,
    Borrow_Date DATE,
    FOREIGN KEY (c_id) REFERENCES customers(c_id),
    FOREIGN KEY (b_id) REFERENCES books(b_id),
    PRIMARY KEY (c_id, b_id)
);

CREATE TABLE customers_books_history (
    c_id INT,
    b_id INT,
    date_borrowed DATE,
    date_returned DATE default '9999-12-31',
    PRIMARY KEY (c_id, b_id, date_borrowed),
    FOREIGN KEY (c_id) REFERENCES customers(c_id),
    FOREIGN KEY (b_id) REFERENCES books(b_id)
);