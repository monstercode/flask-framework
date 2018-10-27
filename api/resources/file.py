from flask_restful import reqparse
from api.common.resources import BaseResource, ProtectedResource
from api.config.config import config
from api.app import api
import os
import uuid
import werkzeug
import importlib
import re
from flask import send_file

#FileManager = importlib.import_module('os.path')


class File(ProtectedResource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('filename', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()

        if not re.match("^[A-Za-z0-9]+?$", data['filename']):
            return {'message':'Invalid filename',
                    'status':'error'
                    }
        file_path = config["UPLOAD_METHOD"]["path"]+"/"+data['filename']
        print(file_path)
        if os.path.isfile(file_path):
            #response = 5
            response = send_file(file_path)
            print(type(response))
            response.headers['content-type'] = 'application/octet-stream'
            return response, 200
        else:
            return {'message':'File not found', 'status':'error' }, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.FileStorage, location='files')
        data = parser.parse_args()

        print(data)
        if data['file'] == "":
            return {
                    'data':'',
                    'message':'No file found',
                    'status':'error'
                    }
        file = data['file']

        if file:
            filename = uuid.uuid4().hex
            file.save(os.path.join(config["UPLOAD_METHOD"]["path"],filename))
            return {
                    'data':filename,
                    'message':'file uploaded',
                    'status':'success'
                    }

        return {'data':'', 'message':'Something went wrong', 'status':'error' }
