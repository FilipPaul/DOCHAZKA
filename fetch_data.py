from urllib.request import urlopen


class FetchData:
    def __init__(self, link = "http://192.168.1.144/logs", logs = "logs.txt"):
        self.link = link
        self.logs = logs

    def fetch_data(self):
        f = urlopen(self.link)
        myfile = f.read()
        with open(self.logs, "wb") as outputfile:
            outputfile.write(myfile)

    def fetch_tags(self):
        f = urlopen("http://192.168.1.144/tags")
        myfile = f.read()
        with open("tags.txt", "wb") as outputfile:
            outputfile.write(myfile)



if __name__ == "__main__":
    link = "http://192.168.1.144/logs"
    data = FetchData()
    data.fetch_data()
    data.fetch_tags()
