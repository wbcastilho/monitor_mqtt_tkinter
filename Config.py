class Config:
    def __init__(self, server="127.0.0.1", port="1883", topic="", process="", topic_service=""):
        self.server = server
        self.port = port
        self.topic = topic
        self.process = process
        self.topic_service = topic_service
