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
            <div class="col-lg-3 col-md-6">
                <div class="tile">
                    <h3>Policies</h3>
					<p>Privacy with small errors.</p>
                    <div class="center-content">
					    <div style="font-size: 36px;">{{policies}}</div>
					</div>
					<div class="tile-footer">
					    <a href="/policies" class="btn btn-link btn-block">Details</a>
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


_policies = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FedMed Server</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1>FedMed Server</h1>
            {{ state | safe }}
            <table class="table">
                <thead>
                    <tr>
                        <th>Policy</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {% for key, description in items%}
                    <tr>
                        <td class="col-md-3">{{ key | safe }}</td>
                        <td>{{ description | safe }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
"""
