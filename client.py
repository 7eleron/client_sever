import requests
import json


def main():
    url = "http://localhost:4000/jsonrpc"

    payload = {
        "method": "callPortMethod",
        "params": ["Advantech", "PCI-1602B", "RS422", "connect"],
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(url, json=payload).json()
    print(response)
    assert response["result"]
    assert response["jsonrpc"]
    assert response["id"] == 1

if __name__ == "__main__":
    main()
