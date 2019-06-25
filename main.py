import templateParser

def main():
    base = "testing"
    arr = [1,2,3,4,5]
    test = False
    parse = templateParser.Parser(locals())
    parse.parseDocument("test.html")
  
if __name__== "__main__":
  main()
