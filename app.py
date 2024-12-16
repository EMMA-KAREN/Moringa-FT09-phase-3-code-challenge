from database.setup import create_tables
from database.connection import get_db_connection
# `from models.article import Article` is importing the `Article` class from the `article` module
# within the `models` package. This allows you to use the `Article` class in your current Python
# script. The `Article` class likely represents the structure and behavior of an article entity in
# your application, and by importing it, you can create instances of the `Article` class and work with
# article objects in your script.
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def delete_record():
    """
    Provides the user with options to delete a magazine, author, or article from the database.
    """
    print("\nDelete Options:")
    print("1. Delete Magazine")
    print("2. Delete Author")
    print("3. Delete Article")
    choice = input("Enter your choice (1/2/3): ")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if choice == "1":
            magazine_id = input("Enter the ID of the magazine to delete: ")
            cursor.execute("DELETE FROM magazines WHERE id = ?", (magazine_id,))
            print(f"Magazine with ID {magazine_id} deleted successfully.")

        elif choice == "2":
            author_id = input("Enter the ID of the author to delete: ")
            cursor.execute("DELETE FROM authors WHERE id = ?", (author_id,))
            print(f"Author with ID {author_id} deleted successfully.")

        elif choice == "3":
            article_id = input("Enter the ID of the article to delete: ")
            cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
            print(f"Article with ID {article_id} deleted successfully.")

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

        conn.commit()

    except Exception as e:
        print(f"An error occurred while deleting the record: {e}")

    finally:
        conn.close()

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()


    '''
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implmentation.
    '''

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid # Use this to fetch the id of the newly created magazine

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models

    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

    print("\nAuthors:")
    for author in authors:
        print(Author(author["id"], author["name"]))

    print("\nArticles:")
    for article in articles:
        print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))

    #   # Update functionality example
    # new_author_name = input("Enter new name for the author: ")
    # author.update_name(new_author_name)
    
    # Delete records
    delete_record()
if __name__ == "__main__":
    main()
