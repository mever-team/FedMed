from flask import Flask, request, jsonify, render_template_string
import yaml
import sys
import importlib
from fedmed.core import templates
from fedmed.privacy import CombinedPolicy


class Server:
    def purpose(self, key):
        if ":" not in key:
            return [key, '<span class="badge bg-info text-dark">Raw</span>']
        fragment, request = key.split(":", 1)
        return [fragment, request.replace("_", "")]

    def desc(self, value):
        if isinstance(value, list) or isinstance(value, dict):
            return "JSON"
        return value.__class__.__name__

    def on_update(self, fragment):
        if fragment in self.history:
            self.history.remove(fragment)
        self.history.append(fragment)
        if len(self.history) > self.memory:
            name = self.history.pop(0)
            del self.fragments[name]

    def __init__(self, config="config.yaml", memory=30, policy=None):
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
        self.memory = memory
        self.history = list()

        # create the app
        self.app = Flask(__name__)

        @self.app.route("/")
        def home():
            return render_template_string(
                templates._index,
                config=self.path,
                operations=len(self.config["methods"]),
                policies=len(self.policy.policies),
                percmemory=int(100 * len(self.history) / self.memory),
                memory=len(self.history),
                maxmemory=self.memory,
            )

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
            return render_template_string(
                templates._data,
                state=f"Cache usage {len(self.history)}/{self.memory}",
                items=[
                    self.purpose(k) + [self.desc(v)] for k, v in self.fragments.items()
                ],
            )

        @self.app.route("/policies", methods=["GET"])
        def policies():
            return render_template_string(
                templates._policies,
                state=f'<div style="margin-bottom: 20px;">Sequentially applied policies loaded from <a href="/config">{self.path}</a>.</div>',
                items=[
                    [p.name(), p.description().replace("\n", " ")]
                    for p in self.policy.policies
                ],
            )

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
            if "other" in kwargs:
                fragment1 = self.fragments[fragment]
                for item in subpoint:
                    if item not in fragment1:
                        return jsonify(f"Item {item} does not exist"), 400
                    fragment1 = fragment1[item]
                if isinstance(kwargs["other"], list):
                    fragment2 = self.fragments[fragment]
                    for item in kwargs["other"]:
                        if item not in fragment2:
                            return jsonify(f"Item {item} does not exist"), 400
                        fragment2 = fragment2[item]
                    subpoint2_alias = ".".join(kwargs["other"])
                else:
                    fragment2 = kwargs["other"]
                    subpoint2_alias = fragment2
                new_name = (
                    f"{fragment}:{method}({'.'.join(subpoint)}, {subpoint2_alias})"
                )
                method = self.config["methods"][method]
                assert isinstance(method, str)
                package, method = method.rsplit(".", 1)
                importlib.__import__(package)
                method = getattr(sys.modules[package], method)
                try:
                    self.fragments[new_name] = method(fragment1, fragment2)
                except Exception as e:
                    print(str(e))
                    return jsonify(str(e)), 400
                self.on_update(new_name)
                return jsonify(new_name), 200
            fragment = self.fragments[fragment]
            method = self.config["methods"][method]["map"]
            package, method = method.rsplit(".", 1)
            importlib.__import__(package)
            method = getattr(sys.modules[package], method)
            for item in subpoint:
                if item not in fragment:
                    return jsonify(f"Item {item} does not exist"), 400
                fragment = fragment[item]
            result = method(fragment, self.policy, **kwargs)
            return jsonify(result), 200

    def __setitem__(self, key, value):
        assert ":" not in key, "Fragment name should not contain ':'."
        assert "?" not in key, "Fragment name should not contain '?'."
        assert "/" not in key, "Fragment name should not contain '/'."
        self.fragments[key] = value

    def run(self, debug=False):
        self.app.run(debug=debug)
