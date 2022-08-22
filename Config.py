class Config:
    def __init__(self, server="127.0.0.1", port="1883", application_topic="", process="", service_topic=""):
        self.server = server
        self.port = port
        self.application_topic = application_topic
        self.process = process
        self.service_topic = service_topic
