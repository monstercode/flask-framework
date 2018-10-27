from flask_restful import Resource

class Project(Resource):
    def get(self, id):
        return {"id": 77}
        #return {todo_id: todos[todo_id]}

    def put(self, id):
        #todos[todo_id] = request.form['data']
        return {message: 'ok'}