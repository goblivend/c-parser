import json

class Position :
    def __init__(self, x, y) :
        self.x = x
        self.y = y

class Node :
    def __init__(self, id,type, data, x, y, width, height) :
        self.id = id
        self.type = type
        self.data = data
        self.position = Position(x, y)
        self.width = width
        self.height = height

class Edge :
    def __init__(self, sourceId, sourceHandle, targetId, targetHandle) :
        self.sourceId = sourceId
        self.sourceHandle = sourceHandle
        self.targetId = targetId
        self.targetHandle = targetHandle

class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {'id': obj.id, 'type': obj.type, 'position': obj.position, 'data':obj.data, 'width': obj.width, 'height': obj.height, 'selected': False, 'positionAbsolute': obj.position, 'dragging': False}
        elif isinstance(obj, Position):
            return {'x': obj.x, 'y': obj.y}
        elif isinstance(obj, Edge):
            return {"source": obj.sourceId, "sourceHandle": obj.sourceHandle, "target": obj.targetId, "targetHandle": obj.targetHandle, "id": f"reactflow__edge-{obj.sourceId}{obj.sourceHandle}-{obj.targetId}{obj.targetHandle}"}
        return json.JSONEncoder.default(self, obj)
