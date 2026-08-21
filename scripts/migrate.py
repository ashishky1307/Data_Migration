import json
from datetime import datetime

import requests
from sqlalchemy import create_engine, text
from model import engine

KAIROS_URL = "http://localhost:8080/api/v1/datapoints/query"

payload = {
    "start_absolute": 1785522782000,
    "end_absolute": 1787120503000,
    "metrics": [
        {
            "name": "project_103__ilens.live_data.raw",
            "group_by": [
                {
                    "name": "tag",
                    "tags": ["c3"]
                }
            ]
        }
    ]
}

response = requests.post(
    KAIROS_URL,
    json=payload,
    headers={"Content-Type": "application/json"}
)

response.raise_for_status()

data = response.json()

results = data["queries"][0]["results"]

count = 0

with engine.begin() as conn:

    for metric in results:

        tag_id = metric["group_by"][0]["group"]["c3"]
        for ts, value in metric["values"]:

            conn.execute(
                text("""
                    INSERT INTO metrics
                    (
                        time,
                        tag_id,
                        metric_name,
                        value
                    )
                    VALUES
                    (
                        :time,
                        :tag_id,
                        :metric_name,
                        :value
                    )
                    ON CONFLICT DO NOTHING
                """),
                {
                    "time": datetime.fromtimestamp(ts / 1000),
                    "tag_id": tag_id,
                    "metric_name": metric["name"],
                    "value": value
                }
            )

            count += 1

print(f"\n{count} records migrated")