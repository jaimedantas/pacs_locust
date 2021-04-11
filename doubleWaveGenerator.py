import math
from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape



def tick(second):
    return (1, 1)


def main():
    for i in range(0,10):
        print("e"+str(tick(i)))

if __name__ == "__main__":
    main()