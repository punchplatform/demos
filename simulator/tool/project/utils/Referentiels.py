import json
import datetime
from elasticsearch import Elasticsearch, helpers


def load_json_file(path):
    data = []
    file = open(path, "r")
    for line in file.readlines():
        data.append(json.loads(line))
    return data


def write_to_es(datas, index, nodes, port, bulk_size, login, password):
    client: Elasticsearch = Elasticsearch(
        nodes=nodes, port=port, http_auth=(login, password)
    )
    actions: List = [
        {"_index": index, "_source": {**data, "@timestamp": datetime.datetime.utcnow()}}
        for data in datas
    ]
    helpers.bulk(
        client=client, actions=actions, chunk_size=bulk_size, request_timeout=60
    )


if __name__ == "__main__":

    print("Push Referentiels")
    datas = load_json_file("/data/world_map.json")
    datas[0]["transform"]["translate"][0] = float(datas[0]["transform"]["translate"][0])
    write_to_es(datas, "world-map", "localhost", "9200", 100, "", "")
