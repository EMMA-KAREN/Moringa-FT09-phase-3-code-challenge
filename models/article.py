from database.connection import get_db_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author=None, magazine=None):
        """
        Initialize an Article instance.

        :param id: The ID of the article (optional, fetched from the database if not provided).
        :param title: The title of the article.
        :param content: The content of the article.
        :param author: An Author instance, representing the author of the article.
        :param magazine: A Magazine instance, representing the magazine associated with the article.
        """
        self._id = id
        self._title = title
        self._content = content
        self._author = author
        self._magazine = magazine

        # If id is None, create a new entry in the database
        if id is None:
            self._create_article_in_db()

    def __repr__(self):
        """
        String representation of the Article instance.
        """
        return f'<Article {self.title}>'

    def _create_article_in_db(self):
        if not isinstance(self.title, str) or not (5 <= len(self.title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")

        # Import deferred to avoid circular import
        from models.author import Author
        from models.magazine import Magazine

        if not isinstance(self.author, Author) or not isinstance(self.magazine, Magazine):
            raise ValueError("Author and Magazine must be valid instances.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
            """,
            (self.title, self.content, self.author.id, self.magazine.id)
        )
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @property
    def id(self):
        """
        Return the ID of the article.
        """
        return self._id
    
    @property
    def author(self):
        from models.author import Author
        return self._author

    @property
    def magazine(self):
        from models.magazine import Magazine
        return self._magazine

    @property
    def title(self):
        """
        Return the title of the article.
        """
        return self._title

    @title.setter
    def title(self, value):
        """
        Prevent changing the title after initialization.
        """
        raise AttributeError("Title cannot be changed after initialization.")

    @property
    def content(self):
        """
        Return the content of the article.
        """
        return self._content

    @content.setter
    def content(self, value):
        """
        Allow updating the content of the article.
        """
        self._content = value

    # @staticmethod
    # def search_by_title(title):
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM articles WHERE title LIKE ?", ('%' + title + '%',))
    #     articles_data = cursor.fetchall()
    #     conn.close()
    #     return [Article(id=data["id"], title=data["title"], content=data["content"], 
    #                     author=Author(id=data["author_id"], name=data["author_name"]),
    #                     magazine=Magazine(id=data["magazine_id"], name=data["magazine_name"], category=data["magazine_category"])) 
    #             for data in articles_data]  

    @property
    def author(self):
        """
        Return the Author instance associated with this article.
        Use SQL JOIN to fetch the author from the database if not already set.
        """
        from models.author import Author
        if not hasattr(self, "_author"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT authors.* FROM authors
                JOIN articles ON articles.author_id = authors.id
                WHERE articles.id = ?
                """,
                (self.id,)
            )
            author_data = cursor.fetchone()
            conn.close()

            if author_data:
                self._author = Author(id=author_data["id"], name=author_data["name"])

        return self._author

    @property
    def magazine(self):
        """
        Return the Magazine instance associated with this article.
        Use SQL JOIN to fetch the magazine from the database if not already set.
        """
        from models.magazine import Magazine
        if not hasattr(self, "_magazine"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT magazines.* FROM magazines
                JOIN articles ON articles.magazine_id = magazines.id
                WHERE articles.id = ?
                """,
                (self.id,)
            )
            magazine_data = cursor.fetchone()
            conn.close()

            if magazine_data:
                self._magazine = Magazine(
                    id=magazine_data["id"],
                    name=magazine_data["name"],
                    category=magazine_data["category"]
                )

        return self._magazine
