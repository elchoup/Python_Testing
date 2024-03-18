from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "test@example.com"})

    @task
    def book(self):
        self.client.get("/book/Fall%20Classic/Simply%20Lift")

    @task
    def purchase_places(self):
        data = {
            "competition": "Fall Classic",
            "club": "Simply Lift",
            "places": "3"
        }
        self.client.post("/purchasePlaces", data=data)

    @task
    def logout(self):
        self.client.get("/logout")