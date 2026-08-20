import json
from datetime import datetime

import requests
from sqlalchemy import text

from model import engine

payload = {
    "start_absolute": 1785522782000,
    "end_absolute": 1787120503000,
    "metrics": [
        {
            "name": "project_103__ilens.live_data.raw"
        }
    ]
}

response = requests.post(
    "http://localhost:8080/api/v1/datapoints/query",
    json=payload
)

response.raise_for_status()

data = response.json()

print(json.dumps(data, indent=2)[:5000])

results = data["queries"][0]["results"]

count = 0

with engine.begin() as conn:

    for metric in results:

        print(f"Metric: {metric['name']}")
        print(f"Datapoints: {len(metric['values'])}")

        for ts, value in metric["values"]:

            conn.execute(
                text("""
                    INSERT INTO metrics
                    (
                        time,
                        metric_name,
                        value,
                        tags
                    )
                    VALUES
                    (
                        :time,
                        :metric_name,
                        :value,
                        CAST(:tags AS JSONB)
                    )
                    ON CONFLICT DO NOTHING
                """),
                {
                    "time": datetime.fromtimestamp(ts / 1000),
                    "metric_name": metric["name"],
                    "value": value,
                    "tags": json.dumps(metric.get("tags", {}))
                }
            )

            count += 1

print(f"\n{count} records migrated")