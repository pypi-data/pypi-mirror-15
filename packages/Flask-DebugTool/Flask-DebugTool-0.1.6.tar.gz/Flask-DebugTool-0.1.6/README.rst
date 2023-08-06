Flask Debugtool
===================

flask-debugtool


Installation
------------

Installing is simple with pip::

    $ pip install flask-debugtool


Usage
-----

Setting up the debug toolbar is simple::

    from flask import Flask
    from flask_debugtool import DebugTool

    app = Flask(__name__)

    toolbar = DebugTool(app)

