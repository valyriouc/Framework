import requests 
import secret
import flask

class HackeroneApiEndpoints:
    @staticmethod
    def hacktivity() -> str:
        return "hacktivity"

    @staticmethod
    def me_reports() -> str:
        return "me/reports"
    
    @staticmethod 
    def reports(id: int | None = None) -> str:
        return "reports" if id is None else f"reports/{id}"
    
    @staticmethod
    def programs() -> str:
        return "programs"

    @staticmethod
    def program(programName: str) -> str:
        return f"{HackeroneApiEndpoints.programs()}/{programName}"

    @staticmethod   
    def scope(programName: str) -> str:
        return f"programs/{programName}/structured_scopes"
    
    @staticmethod 
    def weaknesses(programName: str) -> str:
        return f"programs/{programName}/weaknesses"
    
class HackeroneApiBuilder:
    def __init__(self):
        self.url = "https://api.hackerone.com/"   
    
        self.hasVersion = False
        self.hasMainTopic = False

    def __with_slash(self):
        self.url += "/"

    def with_version1(self):
        self.url += "v1"
        self.__with_slash()
        self.hasVersion = True
        return self

    def with_hacker(self):
        if not self.hasVersion:
            raise ValueError("Need to specify the version!")
        self.url += "hackers"
        self.__with_slash()
        self.hasMainTopic = True
        return self

    def with_endpoint(self, endpoint: str):
        if not self.hasMainTopic:
            raise ValueError("Need to specify the main topic!")
        self.url += endpoint
        if endpoint[len(endpoint) - 1] != "/":
            self.__with_slash()
        return self
    
    def build(self) -> str:
        url = self.url
        self.url = "https://api.hackerone.com/"
        return url

app = flask.Flask(__name__)

@app.route("/api/programs/")
def programs():
    page_index = flask.request.args.get("pageIndex")
    page_size = flask.request.args.get("pageSize")

    builder = HackeroneApiBuilder()

    url = builder.with_version1().with_hacker().with_endpoint(HackeroneApiEndpoints.programs()).build()
    url = f"{url}?page[number]={page_index}&page[size]={page_size}"

    auth = requests.auth.HTTPBasicAuth("valacor", secret.HACKERONE_AT)
    res = requests.get(url, auth=auth)

    content = res.json()
    return [{"handle": program["attributes"]["handle"], "name": program["attributes"]["name"]} for program in content["data"]]

def main(arguments):
    # serving web api 
    if len(arguments) >= 1 and arguments[0] == "serve":
        address = "127.0.0.1"
        port = 7020
        if len(arguments) == 2 and arguments[1] == "tls":
            app.run(address, port+100, ssl_context=("cert.pem", "key.pem"))
        else:
            app.run(address, port)
        return 

    # run as command-line tool
    builder = HackeroneApiBuilder()

    url = builder.with_version1().with_hacker().with_endpoint(HackeroneApiEndpoints.programs()).build()
    auth = requests.auth.HTTPBasicAuth("valacor", secret.HACKERONE_AT)
    res = requests.get(url, auth=auth)

    content = res.json()
    print([program["attributes"]["handle"] for program in content["data"]])

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])