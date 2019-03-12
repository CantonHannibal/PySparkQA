from py2neo import *
from Nodes import *


class QuestionRepository:
    movie = Movie()
    person = Person()
    genre = Genre()
    graph = None
    router = dict()

    def func_Router(self, index: int, *args):
        func = self.router[index]
        return func(*args)

    def __init__(self):
        self.graph = Graph("bolt://localhost:7687", username="neo4j", password="zy34526174")
        self.router[0] = self.getMovieRating
        self.router[1] = self.getMovieReleaseDate
        self.router[2] = self.getMovieTypes
        self.router[3] = self.getMovieInfo
        self.router[4] = self.getMovieActors
        self.router[5] = self.getActorInfo
        self.router[6] = self.getActorMoviesByType
        self.router[7] = self.getActorMovies
        self.router[8] = self.getActorMoviesByHScore
        self.router[9] = self.getActorMoviesByLScore
        self.router[10] = self.getActorMoviesType
        self.router[11] = self.getMoviesCooperatedBy
        self.router[12] = self.getMoviesCount
        self.router[13] = self.getActorBirth

    def getMovie(self, title: str):
        s = "_.title='{title}'"
        s = s.format(title=title)
        a = Movie.match(self.graph).where(s).first()
        return a

    def getMovieRating(self, title: str):
        s = "_.title='{title}'"
        s = s.format(title=title)
        a = Movie.match(self.graph).where(s).first()
        return a.getRating()

    def getMovieReleaseDate(self, title: str):
        s = "_.title='{title}'"
        s = s.format(title=title)
        a = Movie.match(self.graph).where(s).first()
        return a.getReleaseDate()

    def getMovieTypes(self, title: str):
        s = "match(a:Movie)-[b:is]->(c:Genre) where a.title='{title}'  return c.name"
        s = s.format(title=title)
        c = self.graph.run(s).data()
        type_list = list()
        for name in c:
            type_list.append(name['c.name'])

        return type_list

    def getMovieInfo(self, title: str):
        s = "_.title='{title}'"
        s = s.format(title=title)
        a = Movie.match(self.graph).where(s).first()
        if a !=None:
            return a.getIntroduction()
        else:
            return "不知道"

    def getMovieActors(self, name: str):
        s = "match(a:Person)-[b:actedin]->(c:Movie) where c.title='{title}'  return a.name"
        s = s.format(title=name)
        c = self.graph.run(s).data()
        actor_list = list()
        for name in c:
            actor_list.append(name['a.name'])
        return actor_list

    def getActorInfo(self, name: str):
        s = "_.name='{name}'"
        s = s.format(name=name)
        a = Person.match(self.graph).where(s).first()
        if a !=None:
            return a.getName() + " " + a.getBirth() + " " + a.getBiography()
        else:
            return "不知道"

    def getActorMoviesByType(self, name: str, type: str):
        s = "match(a:Person)-[b:actedin]->(c:Movie)-[m:is]->(l:Genre) where a.name='{name}' and l.name='{type}' return c.title"
        s = s.format(name=name, type=type)
        c = self.graph.run(s).data()
        movies_list = list()
        for name in c:
            movies_list.append(name['c.title'])
        return movies_list

    def getActorMovies(self, name: str):
        s = "match(a:Person)-[b:actedin]->(c:Movie) where a.name='{name}' return c.title"
        s = s.format(name=name)
        c = self.graph.run(s).data()
        movies_list = list()
        for name in c:
            movies_list.append(name['c.title'])
        return movies_list

    def getActorMoviesByHScore(self, name: str, scores: float):
        s = "match(a:Person)-[b:actedin]->(c:Movie) where a.name='{name}' and c.rating >{scores} return c.title"
        s = s.format(name=name, scores=scores)
        c = self.graph.run(s).data()
        movies_list = list()
        for name in c:
            movies_list.append(name['c.title'])
        return movies_list

    def getActorMoviesByLScore(self, name: str, scores: float):
        s = "match(a:Person)-[b:actedin]->(c:Movie) where a.name='{name}' and c.rating <{scores} return c.title"
        s = s.format(name=name, scores=scores)
        c = self.graph.run(s).data()
        movies_list = list()
        for name in c:
            movies_list.append(name['c.title'])
        return movies_list

    def getActorMoviesType(self, name: str):
        s = "match(a:Person)-[b:actedin]->(c:Movie)-[m:is]->(l:Genre) where a.name='{name}' return distinct l.name"
        s = s.format(name=name)
        c = self.graph.run(s).data()
        movies_list = list()
        for name in c:
            movies_list.append(name['l.name'])
        print(movies_list)

    def getMoviesCooperatedBy(self, name1: str, name2: str):
        s = "match(a1:Person)-[b1:actedin]->(c1:Movie) where a1.name='{name1}' " \
            "with c1 match(a2:Person)-[b2:actedin]->(c1:Movie) where a2.name='{name2}' return c1.title"
        s = s.format(name1=name1, name2=name2)
        c = self.graph.run(s).data()
        movies_list = list()
        for name in c:
            movies_list.append(name['c1.title'])
        return movies_list

    def getMoviesCount(self, name: str):
        s = "match(a:Person)-[b:actedin]->(c:Movie) where a.name='{name}' return count(*)"
        s = s.format(name=name)
        c = self.graph.run(s).data()
        return c[0]['count(*)']

    def getActorBirth(self, name: str):
        s = "match(a:Person) where a.name='{name}' return a.birth"
        s = s.format(name=name)
        c = self.graph.run(s).data()
        return c[0]['a.birth']
