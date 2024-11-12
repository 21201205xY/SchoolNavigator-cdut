from imaplib import Flags

from svgpathtools import svg2paths
import json

paths, attributes = svg2paths("SchoolMap.svg")

scale_level = 0.0
outputPaths = []
outputVertices = []
outputLocations = []

ADDINFO = False
locationInfo = {
"东区操场": 			""
,"香樟": 			""
,"图书馆": 			""
,"东区二教": 			""
,"东区一教": 			""
,"东门": 			""
,"东区后街": 			""
,"艺术大楼": 			""
,"自然博物馆门": 			""
,"农贸": 			""
,"后街": 			""
,"计科院": 			""
,"商学院": 			""
,"珙桐园": 			""
,"松林园": 			""
,"实验大楼": 			""
,"银杏园": 			""
,"银杏餐厅": 			""
,"沉积地质研究院": 			""
,"八教": 			""
,"九教": 			""
,"地规院": 			""
,"现代教学大楼": 			""
,"二教": 			""
,"芙蓉": 			""
,"芙蓉餐厅": 			""
,"砚湖图书馆": 			""
,"体育学院": 			""
,"西区操场": 			""
,"网球场": 			""
,"篮球场": 			""
,"榕树园": 			""
,"西门": 			""
,"西北门": 			""
,"理工大学地铁口": 			""
}

for i in range(len(paths)):
    if "r" not in attributes[i].keys():
        if (paths[i].end is None) or (paths[i].start is None):
            continue
        outputPaths.append(paths[i])
    else:
        if attributes[i]["r"] == "1.27":   # 如果改了节点的名称，这里要改为 data-name 的判断方式
            outputVertices.append(attributes[i])
        else:
            outputLocations.append(attributes[i])



pathCount = 0
verticeCount = 0

graph = {
    "Vertices": [],
    "Paths": [],
    "Locations": []
}

for i in outputVertices:
    graph["Vertices"].append({
        "Id": verticeCount,
        "Name": 0,  # TODO: Vertice 节点，Name字段可更改
        "X": float(i["cx"]),  # 这里事后debug一下，存储float值还是str值
        "Y": float(i["cy"]),
    })
    verticeCount += 1


def findVerticeId(source, point):
    for vertices in source:
        for i in vertices:
            if i["X"] == point[0] and i["Y"] == point[1]:
                return i["Id"]


def getXY(point):
    result = str(point)[1:-2].split('+')
    return (float(result[0]), float(result[1]))


def getPathStart(path):
    if path.start is None:
        return 0
    return getXY(path.start)


def getPathEnd(path):
    if path.end is None:
        return 0
    return getXY(path.end)


for i in outputPaths:
    graph["Paths"].append({
        "Id": pathCount,
        "Name": f"Path_{pathCount}", # TODO: Path，Name字段可更改
        "Distance": i.length(),
        "StartVerticeId": -1,
        "EndVerticeId": -1,
        "Data": i.d(),
        "IsEnabled": True,
    })
    pathCount += 1


# findVerticeId([graph["Vertices"], graph["Locations"]], getPathStart(i))
# findVerticeId([graph["Vertices"], graph["Locations"]], getPathEnd(i))
for i in outputLocations:
    graph["Locations"].append({
        "Id": verticeCount,
        "Name": i["id"],
        "Info": "" if ADDINFO else locationInfo[i["id"]],
        "X": float(i["cx"]),  # 这里事后debug一下，存储float值还是str值
        "Y": float(i["cy"]),
        "LocatedVerticeIds": [],
        "LocatedPathIds": [],
    })
    verticeCount += 1

for i in range(len(graph["Paths"])):
    graph["Paths"][i]["StartVerticeId"] = findVerticeId([graph["Vertices"], graph["Locations"]], getPathStart(outputPaths[i]))
    graph["Paths"][i]["EndVerticeId"] = findVerticeId([graph["Vertices"], graph["Locations"]], getPathEnd(outputPaths[i]))



# def findLocationAndVerticeId(locations, vertices, path):
#     locationId = -1
#     verticeId = -1
#     if findVerticeId(locations, getPathStart(path)) == None:
#         locationId = findVerticeId(locations, getPathEnd(path))
#         verticeId = findVerticeId(vertices, getPathStart(path))
#     else:
#         locationId = findVerticeId(locations, getPathStart(path))
#         verticeId = findVerticeId(vertices, getPathEnd(path))

#     return locationId, verticeId

# for i in outputRelated:
#     locationId, verticeId = findLocationAndVerticeId(graph["Locations"], graph["Vertices"], i)
#     graph["Paths"].append({
#         "Id": pathCount,
#         "Name": f"Path_{pathCount}",     # TODO: Related 路径，Name字段可更改
#         "Distance": i.length(),
#         "StartVerticeId": locationId,
#         "EndVerticeId": verticeId,
#         "IsRelated": True,
#     })
#     pathCount += 1


def getRelatedVerticesAndPaths(location):
    vertices = []
    paths = []
    for path in graph["Paths"]:
        if path["StartVerticeId"] == location["Id"]:
            vertices.append(path["EndVerticeId"])
            paths.append(path["Id"])
        elif path["EndVerticeId"] == location["Id"]:
            vertices.append(path["StartVerticeId"])
            paths.append(path["Id"])


    return vertices, paths


for i in graph["Locations"]:
    locatedVertices, locatedPaths = getRelatedVerticesAndPaths(i)
    i["LocatedVerticeIds"] += locatedVertices
    i["LocatedPathIds"] += locatedPaths


DEBUG = not ADDINFO
if DEBUG:
    jsonString = json.dumps(graph, indent=2, sort_keys=True)
    file = open("""./SchoolNavigator/data/graph.json""", "w")
    file.write(jsonString)
    print("Success.")
else:
    for location in graph["Locations"]:
        print(f',"{location["Name"]}": \t\t\t""')

"""---------------------------------------------------------------------------------------------------"""

# DEPRECATED = True
# if DEPRECATED:
#
#     """以下都是本用于输出 XAML 样式的脚本，现已停用"""
#
#
#     def getPaths(method):
#         result = []
#         for i in range(len(outputPaths)):
#             result.append(method(graph["Paths"][i]["Name"], outputPaths[i].d()))
#         # for i in range(len(outputRelated)):
#         #     result.append(method(graph["Paths"][i + len(outputPaths)]["Name"], outputPaths[i].d()))
#
#         # list[str]
#         return result
#
#
#     def getVertices(method):
#         result = []
#         for vertice in graph["Vertices"]:
#             result.append(
#                 method(vertice["Name"], vertice["X"], vertice["Y"], 1.5)) # 这里设置 vertice 节点的半径
#
#         # list[str]
#         return result
#
#
#     def getLocations(method):
#         result = []
#         for location in graph["Locations"]:
#             result.append(
#                 method(location["Name"], location["X"], location["Y"]))
#
#         # list[str]
#         return result
#
#
#     """---------------------------------------------------------------------------------------------------"""
#
#
#     def getXAMLPath(name, path):
#         return f"""
#     <Path x:Name="{name}" Style="{{StaticResource Route}}">
#         <Path.Data>
#             <PathGeometry Figures="{path}" />
#         </Path.Data>
#     </Path>"""
#
#
#     def getXAMLEllipse(name, x, y, r):
#
#         # SVG 转 XAML 时需要将数值转化，只适用于无边框圆形
#         return f"""
#     <Ellipse x:Name="{name}" Style="{{StaticResource WayPoint}}"
#             Canvas.Left="{x - r}" Canvas.Top="{y - r}"
#             Height="{r * 2}" Width="{r * 2}" />"""
#
#
#     def getXAMLLocation(name, x, y):
#         return f"""
#     <Button x:Name="{name}" Style="{{StaticResource Location}}"
#             Canvas.Left="{x}" Canvas.Top="{y}"
#             Click="Location_OnClick"
#             MouseDoubleClick="Location_OnMouseDoubleClick" />"""
#
#
# EXPORT = False
# if EXPORT:
#     output = open("output.xaml", "w")
#     output.writelines(getPaths(getXAMLPath))
#     output.writelines(getVertices(getXAMLEllipse))
#     output.writelines(getLocations(getXAMLLocation))
#     output.close()

