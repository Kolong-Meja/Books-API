# app/database/query.py

"""
Place for placing your SQL statement for execute it automatically.

This file can be used for creating RAW SQL statement, so you dont have to create dummy data in OpenAPI GUI.
"""

# CREATE STATEMENT AREA!
create_books_table_query = """
CREATE TABLE IF NOT EXISTS Books (
    uuid VARCHAR(36) NOT NULL,
    isbn VARCHAR(13) NULL UNIQUE,
    title VARCHAR(255) NOT NULL UNIQUE,
    author_id VARCHAR(36),
    pages INTEGER NOT NULL,
    publisher VARCHAR(255) NULL,
    published DATE DEFAULT '1970-01-01',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (uuid),
    CONSTRAINT FK_AuthorBook FOREIGN KEY (author_id) REFERENCES Authors(uuid)
)
"""

create_genres_table_query = """
CREATE TABLE IF NOT EXISTS Genres (
    uuid VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (uuid)
)
"""

create_authors_table_query = """
CREATE TABLE IF NOT EXISTS Authors (
    uuid VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (uuid)
)
"""

create_book_genres_table_query = """
CREATE TABLE IF NOT EXISTS BookGenres (
    book_id VARCHAR(36),
    genre_id VARCHAR(36),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_BookGenre FOREIGN KEY (book_id) REFERENCES Books(uuid) ON DELETE CASCADE,
    CONSTRAINT FK_GenreBook FOREIGN KEY (genre_id) REFERENCES Genres(uuid) ON DELETE CASCADE
)
"""
# END OF CREATE STATEMENT AREA!

# INSERT STATEMENT AREA!
insert_books_data_query = """
INSERT INTO 
    Books (uuid, title, author, pages, published)
VALUES
    ('bf23753b-6fac-4736-87fe-0655b81283f1', 'The Arabian Nights', 750, '2011-11-01'),
    ('72cb7b2e-3a4a-41d5-9686-e43a4a984b9c', 'Le Morte d’Arthur', 512, '1485-01-01'),
    ('42d29ca4-7ba0-480b-9ffc-301a22d0ed2b', 'Alice’s Adventures in Wonderland', 128, '2018-08-12')
"""

insert_authors_data_query = """
INSERT INTO
    Authors (uuid, name)
VALUES
    ('dd514790-ee6d-4274-81b4-ab43541ecbff', 'Sir Richard Burton'),
    ('e6b1f631-6611-45f6-ac93-7312dbb084a4', 'Thomas Malory'),
    ('aa4a2b33-404c-40b9-ae56-ad1905b1259a', 'Lewis Carroll')
"""
# END OF INSERT STATEMENT AREA!

# DELETE STATEMENT AREA!
delete_all_books_data_query = """DELETE FROM Books"""
# END OF DELETE STATEMENT AREA!


# SELECT STATEMENT AREA!
select_all_books_data_query = """SELECT * FROM Books"""
# END OF SELECT STATEMENT AREA!

# DROP TABLE STATEMENT AREA!
drop_books_table_query = """DROP TABLE IF EXISTS Books"""
#END OF DROP TABLE STATEMENT AREA!