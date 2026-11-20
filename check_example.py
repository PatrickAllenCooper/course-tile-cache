from app import play
from candidate import admit
from baseline import admit as always

def check():
    home=list(range(8))*3
    path=home+list(range(100,120))+home
    assert play(path, always)==36
    assert play(path, admit)==28
    assert play(list(range(50)), admit)==50

if __name__ == "__main__":
    check()
    print("Worked trace: 36 LRU fetches, 28 candidate fetches")
