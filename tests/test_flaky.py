import random

def test_flaky_timing():
    #this fails ~30% of the time 
    assert random.random() > 0.3