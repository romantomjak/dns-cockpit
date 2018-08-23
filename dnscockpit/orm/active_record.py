

class Query:

    def __init__(self, session: Session):
        self.session = session

    def all(self):
        raise NotImplementedError

    def count(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def exists(self):
        raise NotImplementedError

    def filter(self):
        raise NotImplementedError

    def first(self):
        raise NotImplementedError

    def get(self, pk):
        raise NotImplementedError


class User(Query):

    def get(self, pk):
        return self.session.query(models.User).get(pk)
