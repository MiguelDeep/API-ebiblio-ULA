


tasks = []
task_id = 1

@server.route('/tasks',methods=['POST'])
def create_task():
  global task_id
  data = request.get_json()
  new_task = Task(id=task_id, title=data['title'],description=data['description'],completed=data['completed'])
  task_id += 1
  tasks.append(new_task)
  return jsonify({"message":" Nova tarefa criada com sucesso. "})

@server.route('/tasks',methods=['GET'])
def get_task():
  task_list = [task.to_dict() for task in tasks]
  

  output = {
    "tasks":task_list,
    "Total" : len(task_list)
  }
  
  return jsonify(output)
  

  
@server.route("/tasks/<int:id>",methods=["GET"])
def update_task(id):
  task = None
  for t in tasks:
    if t.id == id:
      return jsonify(t.to_dict())
  return jsonify({"message":"Nao foi possivel encontrar!"}),404

@server.route('/task',methods=["GET"])
def index():
  return "hello world! q iorejrgf"
