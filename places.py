from collections import namedtuple

from fastapi import FastAPI
from graphene import ObjectType, String, Field, Int, Schema
from starlette.graphql import GraphQLApp

RegionValueObject = namedtuple("Region", ["id", "name"])
PlaceValueObject = namedtuple("Place", ["id", "name", "region"])


class Region(ObjectType):
    id = Int()
    name = String()


class Place(ObjectType):
    id = Int()
    name = String()
    region = Field(Region)


class Query(ObjectType):
    place = Field(Place)

    def resolve_place(parent, info):
        return PlaceValueObject(id=1, name='Palace square', region=RegionValueObject(id=1, name='Saint-Petersburg'))


app = FastAPI()
app.add_route("/", GraphQLApp(schema=Schema(query=Query)))
