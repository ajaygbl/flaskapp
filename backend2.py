import requests
import json
from flask import Flask
app = Flask(__name__)

url = 'https://watchpoint-grafana.d.musta.ch/graphql'

headers = {"service" : "argo",
"start" : "1708819200",
"end" : "1709423999",
"Content-Type" : "application/json"}

payload = {"operationName": "OverviewResourceQuery",
"variables": {
    "name": "argo",
    "start": 1711398850,
    "end": 1711571650,
    "limit": 25,
    "role": "argo-production",
    "sortdirection": "descending",
    "sortdimension": "count",
    "filters": [
        {
            "dimension": "role",
            "value": "argo-production"
        },
        {
            "dimension": "async",
            "value": "false"
        }
    ]
},
"query": "query OverviewResourceQuery($name: String!, $start: Int!, $end: Int!, $filters: [ServiceMetricFilter], $limit: Int!, $sortdimension: ServiceMetricNames, $sortdirection: SortByDirections) {\n  service(name: $name, interval: {start: $start, end: $end}) {\n    name\n    metrics(limit: $limit, names: [count, latency_p95_us, latency_p99_us, latency_p50_us, avg_latency_us, fatal_error_count, fatal_error_rate, non_fatal_error_rate, non_fatal_error_count, error_count, error_rate], dimensions: [resource], granularity: all, filters: $filters, sortdimension: $sortdimension, sortdirection: $sortdirection) {\n      points {\n        values {\n          metric\n          value\n          __typename\n        }\n        __typename\n      }\n      dimensions {\n        dimension\n        value\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
}

@app.route("/slo")
def home():
    response2 = requests.post(url, headers=headers, data=json.dumps(payload))
    return response2.json()

