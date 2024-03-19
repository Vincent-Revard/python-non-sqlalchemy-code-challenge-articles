class Article:
    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        type(self).all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        elif not 5 <= len(title) <= 50:
            raise ValueError("title must be between 5 and 50 characters inclusive")
        elif hasattr(self, "_title"):
            raise AttributeError("title is immutable")
        self._title = title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        if not isinstance(author, Author):
            raise TypeError("author must be an Author")
        elif not len(author.name) > 0:
            raise ValueError("author name cannot be empty")
        self._author = author

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, magazine):
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be a Magazine")
        elif not len(magazine.name) > 0:
            raise ValueError("magazine name cannot be empty")
        self._magazine = magazine

class Author:
    all = []

    def __init__(self, name):
        self.name = name
        type(self).all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        elif not len(name) > 0:
            raise ValueError("name cannot be empty")
        elif hasattr(self, "_name"):
            raise AttributeError("name is immutable")
        self._name = name

    def articles(self):
        return [article for article in Article.all if article.author is self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self.articles():
            return None
        elif len(self.articles()) == 1:
            return list({self.articles()[0].magazine.category})
        else:
            return list({article.magazine.category for article in self.articles()})


class Magazine:
    all = []

    def __init__(self, name, category):
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
        return (
            [article.title for article in self.articles()] if self.articles() else None
        )

    def contributing_authors(self):
        contributors = [article.author for article in self.articles()]
        if not len(contributors) > 2:
            None
        else:
            return list(author for author in contributors)

        # article_counts = {}
        # for article in self.articles():
        #     author = article.author
        #     if author in article_counts:
        #         article_counts[author] += 1
        #     else:
        #         article_counts[author] = 1

        # if contributing_authors := [author for author, count in article_counts.items() if count > 2]:
        #     return contributing_authors
        # else:
        #     None

    @classmethod
    def top_publisher(cls):
        try:
            return max(cls.all, key=lambda magazine: len(magazine.articles()) if magazine.articles() else None)
        except Exception as e:
            print(e)
            return None
