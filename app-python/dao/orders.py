from exceptions.notfound import NotFoundException


class OrderDAO:
    def __init__(self, driver):
        self.driver = driver

    def createOrder(self, id, limit = 6, skip = 0):
        # TODO: Get a list of similar people to the person by their id

        return None