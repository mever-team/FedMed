from flask import Flask, request, jsonify
import yaml
import sys
import importlib


class Server:
    def __init__(self, config="config.yaml"):
        # load configuration
        if isinstance(config, str):
            with open(config, "r") as file:
                self.config = yaml.safe_load(file)
        else:
            self.config = config

        self.fragments = dict()

        # create the app
        self.app = Flask(__name__)

        @self.app.route("/")
        def home():
            return "Hello, this is your Flask app!"

        @self.app.route("/<fragment>/<method>", methods=["POST"])
        def process_fragment_method(fragment, method):
            data = request.json
            if data is None:
                subpoint = []
                kwargs = {}
            else:
                subpoint = data["subpoint"]
                kwargs = data["kwargs"]
            if method not in self.config["methods"]:
                return jsonify(f"Method {method} not supported"), 400
            fragment = self.fragments[fragment]
            method = self.config["methods"][method]["map"]
            package, method = method.rsplit(".", 1)
            importlib.__import__(package)
            method = getattr(sys.modules[package], method)
            for item in subpoint:
                if item not in fragment:
                    return jsonify(f"Item {method} does not exist"), 400
                fragment = fragment[item]
            result = str(method(fragment, **kwargs))
            return jsonify(result), 200

    def __setitem__(self, key, value):
        self.fragments[key] = value

    def run(self, debug=False):
        self.app.run(debug=debug)
