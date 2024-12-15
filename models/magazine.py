from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self._id = id
        self._name = name
        self._category = category

        if id is None:
            self._create_magazine_in_db()

    def __repr__(self):
        return f"<Magazine id={self.id} name='{self.name}' category='{self.category}'>"

    def _create_magazine_in_db(self):
        if not isinstance(self.name, str) or not (2 <= len(self.name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(self.category, str) or len(self.category) == 0:
            raise ValueError("Category must be a non-empty string.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category)
        )
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    # Relationship: Get all articles associated with the magazine
    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT articles.* FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
            """,
            (self.id,)
        )
        articles = cursor.fetchall()
        conn.close()
        return [Article(id=article["id"], title=article["title"], author=article["author_id"], magazine=self.id) for article in articles]

    # Relationship: Get all authors contributing to the magazine
    def contributors(self):

        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            """,
            (self.id,)
        )
        authors = cursor.fetchall()
        conn.close()
        return [Author(id=author["id"], name=author["name"]) for author in authors]

