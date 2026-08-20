import json
import requests

KAIROS_URL = "http://localhost:8080/api/v1/datapoints"

with open("kairos_august_json.txt", "r") as f:
    data = json.load(f)

payload = []

for result in data[0]["results"]:
    metric_name = result["name"]  # metric name extraction 
    tags = result.get("tags", {})

    # because tags present in array format but we need in string
    clean_tags = {
        k: str(v[0]) if isinstance(v, list) and len(v) > 0 else str(v)
        for k, v in tags.items()
    }                            

    for timestamp, value in result["values"]:
        payload.append({
            "name": metric_name,
            "timestamp": timestamp,
            "value": value,
            "tags": clean_tags
        })

response = requests.post(
    KAIROS_URL,
    json=payload,
    headers={"Content-Type": "application/json"}
)

print("Status Code:", response.status_code)
print(response.text)