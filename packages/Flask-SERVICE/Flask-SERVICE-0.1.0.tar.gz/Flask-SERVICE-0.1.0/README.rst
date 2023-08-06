flask_service
============================

cmdb api client


Installation
------------

Installing is simple with pip::

    $ pip install flask-service


Usage
-----

Setting up the debug toolbar is simple::

    # CMDB连接配置
    CMDB_API_URL = "http://cmdb.dev.app.ofidc.com:8001"
    CMDB_API_VERSION = "v1"
    CMDB_SECRET_ID = "nhchkywdix357rwd"
    CMDB_SIGNATURE = "2948b1565a333b1b42c913c918633f40"

    from flask import Flask
    from flask_service import Servcie

    app = Flask(__name__)
    cmdb = Servcie("cmdb", app)
