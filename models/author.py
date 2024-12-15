from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        self._id = id
        self._name = name

        if id is None:
            self._create_author_in_db()

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"

    def _create_author_in_db(self):
        if not isinstance(self.name, str) or len(self.name) == 0:
            raise ValueError("Name must be a non-empty string.")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?)", (self.name,)
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

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM articles WHERE author_id = ?", (self.id,)
        )
        articles_data = cursor.fetchall()
        conn.close()
        return [Article(id=data["id"], title=data["title"], content=data["content"]) for data in articles_data]

    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
            """,
            (self.id,)
        )
        magazines_data = cursor.fetchall()
        conn.close()
        return [Magazine(id=data["id"], name=data["name"], category=data["category"]) for data in magazines_data]