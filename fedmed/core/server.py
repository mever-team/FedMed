import json

from flask import Flask, request, jsonify, render_template_string
import yaml
import sys
import importlib
from fedmed.core import templates
from fedmed.privacy import CombinedPolicy
import threading
import psutil
import json


class Server:
    def purpose(self, key):
        if "." not in key:
            return [key, '<span class="badge bg-info text-dark">Raw</span>']
        fragment = key.split(".", 1)[0]
        request = key
        return [fragment, request]#.replace("_", "")]

    def desc(self, value):
        if isinstance(value, list) or isinstance(value, dict):
            return "JSON"
        return value.__class__.__name__

    def on_update(self, fragment, value):
        self.memory_lock.acquire()
        self.fragments[fragment] = value
        if fragment in self.history:
            self.history.remove(fragment)
        self.history.append(fragment)
        self.policy.on(fragment).acknowledge(self, fragment)
        self.memory_lock.release()

    def __init__(self, config="config.yaml", policy=None):
        # load configuration
        if isinstance(config, str):
            self.path = config
            with open(config, "r") as file:
                self.config = yaml.safe_load(file)
        else:
            self.config = config
            self.path = "custom dictionary"

        self.policy = (
            CombinedPolicy(self.config["privacy"]) if policy is None else policy
        )
        assert isinstance(
            self.policy, CombinedPolicy
        ), "Wrap your privacy policy within a CombinedPolicy."
        self.fragments = dict()
        self.history = list()
        self.memory_lock = threading.Lock()

        # create the app
        self.app = Flask(__name__)

        @self.app.route("/")
        def home():
            self.memory_lock.acquire()
            mem = psutil.virtual_memory()
            ret = render_template_string(
                templates._index,
                config=self.path,
                operations=len(self.config["methods"]),
                policies=len(self.policy.policies),
                percmemory=int(100 * mem.used / mem.total),
                memory=int(mem.used/1024/1024/1024),
                maxmemory=int(mem.total/1024/1024/1024),
            )
            self.memory_lock.release()
            return ret

        @self.app.route("/config", methods=["GET"])
        def config():
            with open(self.path, "r") as file:
                ret = file.read()
            return render_template_string(templates._text, text=ret)

        @self.app.route("/ops", methods=["GET"])
        def ops():
            return render_template_string(
                templates._operations,
                state=f'<div style="margin-bottom: 20px;">Operations are declared in <a href="/config">{self.path}</a>.</div>',
                items=[
                    [
                        k,
                        '<span class="badge bg-success text-light">Local</span>'
                        if isinstance(v, str)
                        else '<span class="badge bg-info text-light">Map</span>',
                        v if isinstance(v, str) else v["map"],
                    ]
                    for k, v in self.config["methods"].items()
                ],
            )

        @self.app.route("/data", methods=["GET"])
        def data():
            self.memory_lock.acquire()
            ret = render_template_string(
                templates._data,
                state=f"Cached requests: {len(self.history)}",
                items=[
                    self.purpose(k) + [self.desc(v)] for k, v in self.fragments.items()
                ],
            )
            self.memory_lock.release()
            return ret

        @self.app.route("/policies", methods=["GET"])
        def policies():
            return render_template_string(
                templates._policies,
                state=f'<div style="margin-bottom: 20px;">Sequentially applied policies loaded from <a href="/config">{self.path}</a>.</div>',
                items=[
                    [p.name(), str(p.applied), p.description().replace("\n", " ")]
                    for p in self.policy.policies
                ],
            )

        def manual_request(fragment, method, data, jsonify=json.dumps):
            if data is None:
                subpoint = []
                kwargs = {}
            else:
                subpoint = data["subpoint"]
                kwargs = data["kwargs"]
            if method not in self.config["methods"]:
                return jsonify(f"Method {method} not supported"), 400
            if "other" in kwargs:
                self.memory_lock.acquire()
                fragment1 = self.fragments[fragment]
                for item in subpoint:
                    if item not in fragment1:
                        self.memory_lock.release()
                        return jsonify(f"Item {item} does not exist"), 400
                    fragment1 = fragment1[item]
                if isinstance(kwargs["other"], list):
                    fragment2 = self.fragments[kwargs["other"][0]]
                    for item in kwargs["other"][1:]:
                        if item not in fragment2:
                            self.memory_lock.release()
                            return jsonify(f"Item {item} does not exist"), 400
                        fragment2 = fragment2[item]
                    subpoint2_alias = ".".join(kwargs["other"])
                else:
                    fragment2 = kwargs["other"]
                    subpoint2_alias = fragment2
                if not subpoint:
                    new_name = (
                        f"{fragment}.{method}({subpoint2_alias})"
                    )
                else:
                    new_name = (
                        f"{fragment}.{method}({'.'.join(subpoint)}, {subpoint2_alias})"
                    )
                self.memory_lock.release()
                method = self.config["methods"][method]
                assert isinstance(method, str)
                package, method = method.rsplit(".", 1)
                importlib.__import__(package)
                method = getattr(sys.modules[package], method)
                try:
                    output = method(fragment1, fragment2)
                    self.on_update(new_name, output)
                except Exception as e:
                    print(str(e))
                    return jsonify(str(e)), 400
                return jsonify(new_name), 200
            self.memory_lock.acquire()
            new_name = (
                f"{fragment}.{method}({'.'.join(subpoint)})"
            )
            fragment = self.fragments[fragment]
            method = self.config["methods"][method]["map"]
            package, method = method.rsplit(".", 1)
            importlib.__import__(package)
            method = getattr(sys.modules[package], method)
            for item in subpoint:
                if item not in fragment:
                    return jsonify(f"Item {item} does not exist"), 400
                fragment = fragment[item]
            self.memory_lock.release()
            result = method(fragment, self.policy.on(new_name), **kwargs)
            return jsonify(result), 200

        @self.app.route("/<fragment>/<method>", methods=["POST"])
        def process_fragment_method(fragment, method):
            data = request.json
            return manual_request(fragment, method, data=data, jsonify=jsonify)

        self.manual_request = manual_request

    def __setitem__(self, key, value):
        assert key!="self", "Fragment name should not be 'self' '.'."
        assert "." not in key, "Fragment name should not contain '.'."
        assert "(" not in key, "Fragment name should not contain '('."
        assert ")" not in key, "Fragment name should not contain ')'."
        assert "*" not in key, "Fragment name should not contain '*'."
        assert "?" not in key, "Fragment name should not contain '?'."
        assert "/" not in key, "Fragment name should not contain '/'."
        self.memory_lock.acquire()
        self.fragments[key] = value
        self.memory_lock.release()

    def run(self, debug=False):
        self.app.run(debug=debug)
