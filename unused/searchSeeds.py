import certifi
import urllib3
import crawDomain as craw

url = "https://duckduckgo.com/?q=homeopatia+chile&ia=web"

def getSeeds():
    http = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED",
        ca_certs=certifi.where()
    )

    seeds = http.request("GET", url)
    print(seeds.data)


if __name__ == "__main__":
    getSeeds()