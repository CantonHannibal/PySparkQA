from py2neo import Graph, Node, Relationship, NodeMatcher
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom


# 连接neo4j数据库


class Movie(GraphObject):
    __primarykey__ = 'title'

    mid = Property()
    rating = Property()
    releasedate = Property()
    title = Property()
    introduction = Property()
    genres = list()
    # type = RelatedTo('Genre')

    def __init__(self):
        pass

    def getMid(self):
        return self.mid

    def getRating(self):
        return self.rating

    def getTitle(self):
        return self.title

    def getReleaseDate(self):
        return self.releasedate

    def getIntroduction(self):
        return self.introduction

    def setGenres(self, genres: list):
        self.genres = genres

    def getGenres(self):
        return self.genres


class Person(GraphObject):
    __primarykey__ = 'name'

    name = Property()
    birth = Property()
    pid = Property()
    biography = Property()
    birthplace = Property()
    death = Property()

    def __init__(self):
        pass

    def getName(self):
        return self.name

    def getBirth(self):
        return self.birth

    def getPid(self):
        return self.pid

    def getBiography(self):
        return self.biography

    def getBirthPlace(self):
        return self.birthplace

    def getDeath(self):
        return self.death


class Genre(GraphObject):
    __primarykey__ = 'name'

    name = Property()
    gid = Property()
    # has = RelatedFrom('Movie','TYPE')

    def __init__(self):
        pass

    def getName(self):
        return self.name

    def getGid(self):
        return self.gid


# if __name__ == '__main__':
#     graph = Graph("bolt://localhost:7687", username="neo4j", password="zy34526174")
#     s = "_.title='{title}'"
#
#     s = s.format(title='卧虎藏龙')
#     print(s)
#     a = Movie.match(graph).where(s).first()
#     b = Person.match(graph).where("_.name='巩俐'").first()
#
#     # c=graph.run("match(a:Movie)-[b:is]->(c:Genre) where a.title='2046'  return c.name").data()
#     # for i in graph.match(a,r_type="type"):
#     #     print(i.end_node()["name"])
#     # matcher= NodeMatcher(graph)
#     # a=matcher.match("Person",name='Carina Lau').first()
#     # b=graph.run("MATCH (u:Person{name:'巩俐'}) RETURN u" )
#     print(a.getRating())
#
#     # print(b.getBirth())
#
#     # s = "match(a:Person)-[b:actedin]->(c:Movie) where c.title='{title}'  return a.name"
#     # s = s.format(title='卧虎藏龙')
#     # c = graph.run(s).data()
#     # print(c)
#     # type_list = list()
#     # for name in c:
#     #     type_list.append(name['a.name'])
#     # print(type_list)
#
#
#     # s = "_.name='{name}'"
#     # s = s.format(name='巩俐')
#     # a = Person.match(graph).where(s).first()
#     # print(a.getBiography())
#
#     # s = "match(a:Person)-[b:actedin]->(c:Movie) where a.name='{name}' and c.rating >{scores} return c.title"
#     # s = s.format(name="周星驰", scores=8.0)
#     # print(s)
#     # c = graph.run(s).data()
#     # type_list = list()
#     # for name in c:
#     #     type_list.append(name['c.title'])
#     # print(type_list)
#
#     # s = "match(a:Person)-[b:actedin]->(c:Movie)-[m:is]->(l:Genre) where a.name='{name}' return distinct l.name"
#     # s = s.format(name="周星驰")
#     # c = graph.run(s).data()
#     # movies_list = list()
#     # for name in c:
#     #     movies_list.append(name['l.name'])
#     # print(movies_list)
#
#     # s = "match(a:Person)-[b:actedin]->(c:Movie) where a.name='{name}' return count(*)"
#     # s = s.format(name="周星驰")
#     # c = graph.run(s).data()
#     # print(c[0]['count(*)'])
#
#     # s = "match(a:Person) where a.name='{name}' return a.birth"
#     # s = s.format(name='周星驰')
#     # c = graph.run(s).data()
#     # print( c[0]['a.birth'])
#
#     # def geMoviesCooperatedBy(self,name1:str,name2:str):
#
#     # s = "match(a1:Person)-[b1:actedin]->(c1:Movie) where a1.name='{name1}' " \
#     #     "with c1 match(a2:Person)-[b2:actedin]->(c1:Movie) where a2.name='{name2}' return c1.title"
#     # s = s.format(name1="周星驰",name2="张柏芝")
#     # c = graph.run(s).data()
#     # movies_list = list()
#     # for name in c:
#     #     movies_list.append(name['c1.title'])
#     # print(movies_list)
#
#     s = "match(a:Person)-[b:actedin]->(c:Movie) where c.title='{title}'  return a.name"
#     s = s.format(title="逃学威龙")
#     c = graph.run(s).data()
#     actor_list = list()
#     for name in c:
#         actor_list.append(name['a.name'])
#     print(actor_list)