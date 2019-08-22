import prometheus_client
from flask import Response
from flask_restful import Resource

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


class PrometheusResource(Resource):
    def get(self):
        return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)
