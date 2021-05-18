from flask import Flask, render_template,request, jsonify
from Classes.UCS import UCS
from Classes.AStar import AStar
import re,time
app = Flask(__name__,static_url_path='',
            static_folder='Static',
            template_folder='Templates')
@app.route("/")
def MainPage():
    return render_template("index.html")
@app.route("/stateSpaceSearch",methods = ['POST'])
def StateSpaceSearch():
    spaceSearchResult={}
    spaceSearchAlgo= request.form.getlist('spaceSearchAlgo')
    pattern = re.compile(r'\s+')
    inputSource = re.sub(pattern, '', request.form['source'])
    inputDest = re.sub(pattern, '', request.form['destination'])
    for item in spaceSearchAlgo:
        if(item=="ucs"):
            ucs = UCS("Static/input.txt",inputSource,inputDest)
            start_time = time.perf_counter()
            uscResult=ucs.uniformCostSearch()
            spaceSearchResult["ucs"]={
                "ExecutionTime in Sec":time.perf_counter() - start_time,
                "Path": ','.join(ucs.getRoute(uscResult[1])),
                "TotalCost":uscResult[2]
            }
            del ucs
        else:
            aStar = AStar("Static/input.txt", "Static/heuristic_kassel.txt",inputSource, inputDest)
            start_time = time.perf_counter()
            aStarResult = aStar.aStarSearch()
            spaceSearchResult["astar"]={
                "ExecutionTime in Sec":time.perf_counter() - start_time,
                "Path": ','.join(aStar.getRoute(aStarResult[1])),
                "TotalCost":aStarResult[2]
            }
            del aStar
    return jsonify(spaceSearchResult)
@app.route("/static/<path:filename>")
def GetFile(filename):
    with open("/Static/"+filename, "r") as f:
        content = f.read()
    return render_template(content, mimetype='text/plain')
if __name__ == '__main__':
    app.run(debug=True)