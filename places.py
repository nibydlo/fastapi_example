from collections import namedtuple

from fastapi import FastAPI
from graphene import ObjectType, String, Field, Int, Schema
from starlette.graphql import GraphQLApp

RegionValueObject = namedtuple("Region", ["id", "name"])


class Region(ObjectType):
    id = Int()
    name = String()


class Place(ObjectType):
    id = Int()
    name = String()
    region = Field(Region)

    def resolve_region(parent, info):
        return RegionValueObject(id=1, name='Saint-Petersburg')


app = FastAPI()
app.add_route("/", GraphQLApp(schema=Schema(query=Place)))
