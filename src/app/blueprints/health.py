import os
import requests
from flask import Blueprint, jsonify

from src.app.tasks.normal_tasks import foo2

health = Blueprint('health', __name__)


@health.route('/liveness')
def liveness():
    """
     that it's a router to be used by liveness probe check, that we setup in k8s for monitoring
    the instance.
     A liveness check that fails will trigger a restart of
    a Pod. Liveness checks are generally performed every 10 seconds (but
    this is configurable).
     This behaviour makes this check ideal for making
    sure the app is still running correctly by adding in additional internal
    checks that would trigger a failure of this check in case of problems.
    If this check fails, the Pod will be restarted.
    """
    response = jsonify({"status": 200})
    response.headers['Content-Type'] = 'application/json'
    foo2.delay(1, 2)
    return response, 200


@health.route('/readiness')
def readiness():
    """
    that it's a router to be used by readiness probe check, that check indicates
    whether a Pod is ready to receive traffic.
    Failing a readiness check will not make the Pod restart itself, it will
    just be removed as an EndPoint until the check succeeds again.
    This can be used to allow a container to do some initialisation during startup and
    even to put a Pod in 'maintenance mode'.
    """
    response = jsonify({"status": 200})
    response.headers['Content-Type'] = 'application/json'
    return response, 200
