import msgspec


class Route(msgspec.Struct):
    city1: str
    city2: str
    city3: str


class RouteMap(msgspec.Struct):
    routes: list[Route] = msgspec.field(name="route")


class Origin(msgspec.Struct):
    code: str
    jb: bool
    cc: list[str] = msgspec.field(name="cc", default_factory=list)


class OriginMapData(msgspec.Struct):
    origins: list[Origin]


class OriginMap(msgspec.Struct):
    data: OriginMapData
