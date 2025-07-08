from flask import request, jsonify, Flask, render_template, redirect, url_for

import os
import json

Taskoid = Flask(__name__)

TASK_FILE = "tasks.json"

def load_tasks():
	if os.path.exists(TASK_FILE):
		with open(TASK_FILE, "r") as f:
			return json.load(f)
	return []

def save_tasks():
	with open(TASK_FILE, "w") as f:
		 json.dump(task, f, indent=4)

task = load_tasks()

@Taskoid.route('/')
def home():
    return render_template("index.html", tasks=task)

@Taskoid.route('/add-task', methods=['POST'])
def add_task_form():
    data = request.form
    new_id = len(task) + 1
    new_task = {
        "Task.no.": new_id,
        "Task": data.get("Task", "Untitled"),
        "Status": data.get("Status", "pending")
    }
    
    task.append(new_task)
    save_tasks()
    return redirect(url_for('home'))
    
@Taskoid.route('/tasks', methods=['GET'])
def get_tasks( ):
	return jsonify(task)

@Taskoid.route('/task',methods=['POST'])
def add_tasks( ):
	data = request.get_json( )
	new_id = len(task)+1
	new_task = {
	"Task.no." : new_id ,
	"Task" : data.get("Task","Untitled") ,
	"Status" : data.get("Status","pending")
	}
	
	task.append(new_task)
	save_tasks()
	return jsonify({
	"message" : "Task added!!!",
	"task" : new_task
	}), 201

@Taskoid.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for t in task:
        if t["Task.no."] == task_id:
            task.remove(t)
            save_tasks()
            return jsonify({"message": "Task deleted!"})
    return jsonify({"error": "Task not found"}), 404

@Taskoid.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for t in task:
        if t["Task.no."] == task_id:
            t["Task"] = data.get("Task", t["Task"])
            t["Status"] = data.get("Status", t["Status"])
            save_tasks()
            return jsonify({"message": "Task updated!", "task": t})
            
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
	Taskoid.run(host='0.0.0.0',port=5000, debug=True)
