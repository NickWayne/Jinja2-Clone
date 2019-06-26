from cleanupStaging.rubic2 import Rubic2
from car import car

def main():
    base = "testing"
    arr = [1,2,"HELLO CHAD",4,5]
    dict = [{"Name": {"First": "Nick", "Last": "Wayne"}, "occupation": "Dev"}]
    test = False
    car1 = car()
    parse = Rubic2.Parser(locals())
    parse.parseDocument("testloop.html", "outLoop.html")
  
if __name__== "__main__":
  main()
