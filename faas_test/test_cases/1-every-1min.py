from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
from skimage.io import imread_collection
import base64
import random
import glob

class UserTasks(TaskSet):
    @task
    def get_root(self):
        json = {"fileContents": str(getImage())[2:]}
        self.client.post("/", data=None, json=json)


class WebsiteUser(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]


class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.
    Keyword arguments:
        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage
        stop_at_end -- Can be set to stop once all stages have run.
    """
    threshold = 60
    before = 1
    userIdle = 1
    totalTestTime = 1

    def tick(self):
        run_time_start = self.get_run_time()
        run_time_target = run_time_start + self.threshold
        if run_time_start < run_time_target:
            print("do nothing")
        elif run_time_start == run_time_target:
            print("send request")
            tick_data = (self.userIdle, self.userIdle)
            self.before = self.userIdle
            return tick_data
        elif run_time_start > run_time_target:
            print("updated timer")
            run_time_target += self.threshold


def getImage():
    data = []
    col_dir = 'images_set/sample/*.jpg'
    col = imread_collection(col_dir)

    for filename in glob.glob(col_dir):
        with open(filename, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
        data.append(str(b64_string))

    index = random.randint(0, len(data)-1)
    return data[index]


if __name__ == "__main__":
    print(getImage())