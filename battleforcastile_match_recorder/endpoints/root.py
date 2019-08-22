from flask_restful import Resource


class RootResource(Resource):
    def get(self):
        return 'All systems are working', 200
