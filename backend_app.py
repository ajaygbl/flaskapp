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

payload2 = {
"operationName" : "Slo",
"query": "query Slo($service: String!, $start: Int!, $end: Int!) {\n  service_weekly_slo(service: $service, start: $start, end: $end) {\n    slos\n    __typename\n  }\n  scry_teams: scry_teams_for_project(project_name: $service)\n  endpoints(services: [$service]) {\n    service\n    resource\n    application\n    error_budget\n    uptime(interval: {start: $start, end: $end}) {\n      percent\n      total_minutes\n      violation_minutes\n      __typename\n    }\n    previous_week_uptime(interval: {start: $start, end: $end}) {\n      percent\n      __typename\n    }\n    slos {\n      name\n      title\n      description\n      uptime(interval: {start: $start, end: $end}) {\n        percent\n        __typename\n      }\n      endpoint_id\n      spec\n      spec_format\n      evaluations(interval: {start: $start, end: $end}) {\n        started_at\n        ended_at\n        satisfied\n        slo_id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
"variables" : {"service": "argo", "start": 1708819200, "end": 1709423999}
}

@app.route("/argo")
def home():
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    respJson = response.json()
    return respJson

