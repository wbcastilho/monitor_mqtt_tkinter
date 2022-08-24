import paho.mqtt.client as mqtt
import random


class ClientMqtt:

    def __init__(self, name: str, topic: str, ip="127.0.0.1", port=1883, keepalive=60) -> None:
        self._client = mqtt.Client(name + "_" + str(random.randint(1, 10000)))
        # self._client = mqtt.Client(name)
        self._ip = ip
        self._port = port
        self._keepalive = keepalive
        self._topic = topic
        self._connected = False

        self._client.will_set(self._topic, "1", 1, True)

        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_disconnect = self._on_disconnect

        self._client.connect(ip, port, keepalive)

        self._client.loop_start()

    @property
    def connected(self):
        return self._connected

    def _on_connect(self, client, userdata, flags, rc) -> None:
        try:
            print("MQTT Server conectado com sucesso " + str(rc))
            self._client.publish(self._topic, "0")
            self._connected = True
        except Exception:
            raise Exception('Falha ao conectar ao Broker MQTT.')

    def _on_disconnect(self, client, userdata, rc) -> None:
        if rc != 0:
            self._connected = False
            raise Exception("Cliente desconectado do broker de maneira inesperada.")

    def _on_message(self, client, userdata, msg) -> None:
        pass

    def publish(self, topic: str, value: str):
        try:
            self._client.publish(topic, value)
        except Exception:
            raise Exception('Falha ao realizar publish MQTT.')

    def disconnect(self):
        try:
            self._client.disconnect()
        except Exception:
            raise Exception('Falha ao desconectar do broker MQTT.')

    def loop_stop(self):
        try:
            self._client.publish(self._topic, "1")
            self._client.loop_stop(force=True)
        except Exception:
            raise Exception('Falha ao interromper loop do broker.')

    def loop_stop_and_disconnect(self):
        self.loop_stop()
        self.disconnect()
        self._connected = False
