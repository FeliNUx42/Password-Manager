from modules.manager import Manager
from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

error = json.dumps({
  "data" : None,
  "error" : "Wrong database or database-password..."
})

def ret(data):
  dic = {"data":None, "error":None}
  dic["data"] = data

  if not data:
    dic["error"] = "Nothing found..."
    dic["data"] = None

  return json.dumps(dic)

@app.route("/updateuser", methods=["POST"])
def updateuser():
  m = Manager(request.form["db"], request.form["db_pwd"])

  if not m.isvalid(): return error
  
  data = m.update(request.form["website"], "user", request.form["user"])
  m.close()
  return ret(data)

@app.route("/updatepwd", methods=["POST"])
def updatepwd():
  m = Manager(request.form["db"], request.form["db_pwd"])

  if not m.isvalid(): return error
  
  data = m.update(request.form["website"], "pwd", request.form["pwd"])
  m.close()
  return ret(data)

@app.route("/add", methods=["POST"])
def add():
  m = Manager(request.form["db"], request.form["db_pwd"])

  if not m.isvalid(): return error
  
  data = m.add(request.form["website"], request.form["user"], request.form["pwd"])
  m.close()
  return ret(data)

@app.route("/addrandom", methods=["POST"])
def addrandom():
  m = Manager(request.form["db"], request.form["db_pwd"])

  if not m.isvalid(): return error

  length = request.form["length"]
  try:
      length = int(length)
  except:
      return json.dumps({ "data" : None, "error" : "Length isn't a number..." })
  
  data = m.addrandom(request.form["website"], request.form["user"], length)
  m.close()
  return ret(data)

@app.route("/read", methods=["POST"])
def read():
  m = Manager(request.form["db"], request.form["db_pwd"])

  if not m.isvalid(): return error
  
  data = m.read(request.form["website"])
  m.close()
  return ret(data)

@app.route("/delete", methods=["POST"])
def delete():
  m = Manager(request.form["db"], request.form["db_pwd"])

  if not m.isvalid(): return error
  
  data = m.delete(request.form["website"])
  m.close()
  return ret(data)

@app.route("/readall", methods=["POST"])
def readall():
  m = Manager(request.form["db"], request.form["db_pwd"])

  if not m.isvalid(): return error
  
  data = m.readall()
  m.close()
  return ret(data)

if __name__ == '__main__':
  app.run(port=5000)