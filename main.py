import requests 
import secret

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
     
def main():
    builder = HackeroneApiBuilder()

    url = builder.with_version1().with_hacker().with_endpoint(HackeroneApiEndpoints.programs()).build()
    res = requests.get(url, auth=('valacor', secret.HACKERONE_AT))

    content = res.json()
    print(content)
    
if __name__ == "__main__":
    main()