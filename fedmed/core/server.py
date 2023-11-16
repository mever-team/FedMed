from flask import Flask, request, jsonify, render_template_string
import yaml
import sys
import importlib

_text = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FedMed</title>
</head>
<body>
<pre>
{{text}}
</pre>
</body>
</html>
"""

_index = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>FedMed</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        .tile {
            border: 1px solid #ccc;
            padding: 15px;
            margin-bottom: 20px;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        .tile-footer {
            margin-top: auto;
        }
        .center-content {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            margin-top: -10px;
        }
        .progress {
            height: 36px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
		<h1>FedMed Server</h1>
		<div style="margin-bottom: 20px;">Configurations loaded from <a href="/config">{{config}}</a>.</div>
        <div class="row">
            <div class="col-lg-3 col-md-6">
                <div class="tile">
                    <h3>Operations</h3>
					<p>Callable by clients.</p>
                    <div class="center-content">
					    <div style="font-size: 36px;">{{operations}}</div>
					</div>
					<div class="tile-footer">
					    <a href="/ops" class="btn btn-link btn-block">Details</a>
					</div>
                </div>
            </div>
            <div class="col-lg-3 col-md-12">
                <div class="tile">
                    <h3>Cache</h3>
                    <p>Used by client computations.</p>
                    <div class="center-content">
                        <div class="progress col-lg-12">
                            <div class="progress-bar bg-warning" role="progressbar" style="margin-left: -14px; width: {{percmemory}}%;" aria-valuenow="percmemory"
                                aria-valuemin="0" aria-valuemax="100">{{memory}}/{{maxmemory}}</div>
                        </div>
                    </div>
					<p></p>
					<div class="tile-footer">
					    <a href="/data" class="btn btn-link btn-block">Details</a>
					</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""


_operations = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FedMed Server</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <meta http-equiv="refresh" content="30">
    </head>
    <body>
        <div class="container">
            <h1>FedMed Server</h1>
            {{ state | safe }}
            <table class="table">
                <thead>
                    <tr>
                        <th>Operation</th>
                        <th>Type</th>
                        <th>Implementation</th>
                    </tr>
                </thead>
                <tbody>
                    {% for key, operation, value in items%}
                    <tr>
                        <td>{{ key | safe }}</td>
                        <td>{{ operation | safe }}</td>
                        <td>{{ value | safe }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
"""

_data = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FedMed Server</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <meta http-equiv="refresh" content="30">
    </head>
    <body>
        <div class="container">
            <h1>FedMed Server</h1>
            {{ state | safe }}
            <table class="table">
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Request</th>
                        <th>Value Type</th>
                    </tr>
                </thead>
                <tbody>
                    {% for key, operation, value in items%}
                    <tr>
                        <td>{{ key | safe }}</td>
                        <td>{{ operation | safe }}</td>
                        <td>{{ value | safe }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
"""


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

    def __init__(self, config="config.yaml", memory=30):
        # load configuration
        if isinstance(config, str):
            self.path = config
            with open(config, "r") as file:
                self.config = yaml.safe_load(file)
        else:
            self.config = config
            self.path = "custom dictionary"

        self.fragments = dict()
        self.memory = memory
        self.history = list()

        # create the app
        self.app = Flask(__name__)

        @self.app.route("/")
        def home():
            return render_template_string(_index,
                                          config=self.path,
                                          operations=len(self.config["methods"]),
                                          percmemory=int(100*len(self.history)/self.memory),
                                          memory=len(self.history),
                                          maxmemory=self.memory
                                          )

        @self.app.route("/config", methods=["GET"])
        def config():
            with open(self.path, "r") as file:
                ret = file.read()
            return render_template_string(_text, text=ret)

        @self.app.route("/ops", methods=["GET"])
        def ops():
            return render_template_string(_operations,
                                          state=f'<div style="margin-bottom: 20px;">Configurations loaded from <a href="/config">{self.path}</a>.</div>',
                                          items=[[k, '<span class="badge bg-success text-light">Local</span>' if isinstance(v, str) else '<span class="badge bg-info text-light">Map</span>', v if isinstance(v, str) else v["map"]] for k, v in self.config["methods"].items()])

        @self.app.route("/data", methods=["GET"])
        def data():
            return render_template_string(_data,
                                          state=f"Cache usage {len(self.history)}/{self.memory}",
                                          items=[self.purpose(k) + [self.desc(v)] for k, v in self.fragments.items()])

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
                new_name = f"{fragment}:{method}({'.'.join(subpoint)}, {subpoint2_alias})"
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
            result = method(fragment, **kwargs)
            return jsonify(result), 200

    def __setitem__(self, key, value):
        assert ":" not in key, "Fragment name should not contain ':'."
        assert "?" not in key, "Fragment name should not contain '?'."
        assert "/" not in key, "Fragment name should not contain '/'."
        self.fragments[key] = value

    def run(self, debug=False):
        self.app.run(debug=debug)
