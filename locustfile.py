from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
from skimage.io import imread_collection
import base64
import random
import json
from PIL import Image
import glob

class UserTasks(TaskSet):
    @task
    def get_root(self):
        json = {"fileContents": str(getImage())[2:]}
        #data['fileContents'] = str(getImage())
        #json_data = json.dumps(data)
        self.client.post("/", data=None, json=json)


class WebsiteUser(HttpUser):
    wait_time = constant(0.5)
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
    threshold = 450
    before = 1
    userIdle = 6
    totalTestTime = 9000

    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.threshold:
            tick_data = (self.userIdle, self.userIdle)
            self.before = self.userIdle
            #print("run: "+str(run_time))
            return tick_data
        elif run_time < self.totalTestTime:
            value = 0.006235828 + self.before
            self.before = value
            print("User: "+str(value))
            #print("run: "+str(run_time))
            tick_data = (int(value), int(value))
            return tick_data

        return None


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