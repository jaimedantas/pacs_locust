from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape


class UserTasks(TaskSet):
    @task
    def get_root(self):
        self.client.get("/")


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
    threshold = 120
    before = 1
    userIdle = 6
    totalTestTime = 1200
    totalTestEnd = 1320


    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.threshold:
            tick_data = (self.userIdle, self.userIdle)
            self.before = self.userIdle
            #print("run: "+str(run_time))
            return tick_data
        elif run_time < self.totalTestTime:
            value = 0.056235828 + self.before
            self.before = value
            print("User: "+str(value))
            #print("run: "+str(run_time))
            tick_data = (int(value), int(value))
            return tick_data
        elif run_time < self.totalTestEnd:
            value = self.before - 0.206235828
            self.before = value
            print("User: " + str(value))
            # print("run: "+str(run_time))
            tick_data = (int(value), int(value))
            return tick_data
        return self.userIdle, self.userIdle
