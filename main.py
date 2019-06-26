import templateParserLoop

def main():
    base = "testing"
    arr = [1,2,3,4,5]
    dict = [{"Name": "Nick", "occupation": "Dev"}, {"Name": "Nick", "occupation": "Guitar"}]
    test = False
    parse = templateParserLoop.Parser(locals())
    parse.parseDocument("testloop.html", "outLoop.html")
  
if __name__== "__main__":
  main()
