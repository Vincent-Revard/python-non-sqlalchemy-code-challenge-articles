from collections import Counter


class ArticleInitializationError(Exception):
    pass


class TitleError(Exception):
    pass


class AuthorError(Exception):
    pass


class MagazineError(Exception):
    pass


class Article:
    all = []

    def __init__(self, *args):
        try:
            if len(args) != 3:
                raise ArticleInitializationError(
                    "Article() takes exactly 3 positional arguments, author, magazine, title"
                )
            self.author = args[0]
            self.magazine = args[1]
            self.title = args[2]
            type(self).all.append(self)
        except Exception as e:
            raise ArticleInitializationError(e)

    def __repr__(self):
        return f"Article(author={self.author}, magazine={self.magazine}, title={self.title})"
    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        try:
            if not isinstance(title, str):
                raise TypeError("title must be a string")
            elif not 5 <= len(title) <= 50:
                raise TitleError("title must be between 5 and 50 characters inclusive")
            elif hasattr(self, "_title"):
                raise AttributeError("title cannot change after instantiation")
            self._title = title
        except Exception as e:
            raise TitleError(e)

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        try:
            if not isinstance(author, Author):
                raise TypeError("author must be an Author")
            elif not len(author.name) > 0:
                raise ValueError("author name cannot be empty")
            self._author = author
        except Exception as e:
            raise AuthorError(e)

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, magazine):
        try:
            if not isinstance(magazine, Magazine):
                raise TypeError("magazine must be a Magazine")
            elif not len(magazine.name) > 0:
                raise ValueError("magazine name cannot be empty")
            self._magazine = magazine
        except Exception as e:
            raise MagazineError(e)


class Author:
    all = []

    def __init__(self, name):
        if not name:
            raise AuthorError("Author() requires a non-empty name")
        self.name = name
        type(self).all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        try:
            if not isinstance(name, str):
                raise TypeError("name must be a string")
            elif not len(name) > 0:
                raise ValueError("name cannot be empty")
            elif hasattr(self, "_name"):
                raise AttributeError("name is immutable")
            self._name = name
        except Exception as e:
            raise AuthorError(e)

    def articles(self):
        return [article for article in Article.all if article.author is self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, *args):
        if len(args) != 2:
            raise ValueError("add_article() requires exactly 2 arguments: magazine and title")
        return Article(self, *args)

    def topic_areas(self):
        article_magazine_categories = [
            article.magazine.category for article in self.articles()
        ]
        return (
            list(set(article_magazine_categories))
            if article_magazine_categories
            else None
        )

class Magazine:
    all = []

    def __init__(self, name, category):
        if not all((name, category)):
            raise MagazineError(
                "Magazine() takes exactly 2 positional arguments: name, category"
            )
        self.name = name
        self.category = category
        type(self).all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not 2 <= len(name) <= 16:
            raise ValueError("name must be between 2 and 16 characters inclusive")
        self._name = name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if not isinstance(category, str):
            raise TypeError("category must be a string")
        elif not len(category) > 0:
            raise ValueError("category cannot be empty")
        self._category = category

    def articles(self):
        return [article for article in Article.all if article.magazine is self]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        self_articles = self.articles()
        return [article.title for article in self_articles] if self_articles else None

    def _author_counts(self):
        return Counter(article.author for article in self.articles())

    def author_article_counts(self):
        return self._author_counts()

    def contributing_authors(self):
        author_counts = self._author_counts()
        contributing_authors = [
            author for author, count in author_counts.items() if count > 2
        ]
        return contributing_authors if contributing_authors else None

    @classmethod
    def top_publisher(cls):
        try:
            return max(
                cls.all,
                key=lambda magazine: (
                    len(magazine.articles()) if magazine.articles() else None
                ),
            )
        except Exception as e:
            print(e)
            return None

try:
    # Code that may raise exceptions
    pass
except ArticleInitializationError as e:
    print("Error occurred during article initialization:", e)
except TitleError as e:
    print("Title error:", e)
except AuthorError as e:
    print("Author error:", e)
except MagazineError as e:
    print("Magazine error:", e)
except Exception as e:
    print("An unexpected error occurred:", e)