class Config:
    def __init__(self, server="127.0.0.1", port="1883", application_topic="", service_topic_1="", enable_topic_1=False,
                 service_topic_2="",  enable_topic_2=False, service_topic_3="",  enable_topic_3=False,
                 service_topic_4="",  enable_topic_4=False, service_topic_5="",  enable_topic_5=False):
        self.server = server
        self.port = port
        self.application_topic = application_topic
        self.service_topic_1 = service_topic_1
        self.enable_topic_1 = enable_topic_1
        self.service_topic_2 = service_topic_2
        self.enable_topic_2 = enable_topic_2
        self.service_topic_3 = service_topic_3
        self.enable_topic_3 = enable_topic_3
        self.service_topic_4 = service_topic_4
        self.enable_topic_4 = enable_topic_4
        self.service_topic_5 = service_topic_5
        self.enable_topic_5 = enable_topic_5
