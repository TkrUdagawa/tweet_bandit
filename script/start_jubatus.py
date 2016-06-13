from subprocess import Popen, PIPE
import sys, json

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        jubaconfig = sys.argv[2]
        json_config = json.load(f)
        category_port = json_config["port"]
        Popen(["jubabandit", "-f", sys.argv[2], "-t", "0", "-p", str(category_port)])
        for c in json_config["category"]:
            Popen(["jubabandit", "-f", sys.argv[2], "-t", "0", "-p", str(json_config["category"][c]["port"])])
