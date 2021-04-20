from app.support.base import FileGenerator
from app.support.common.common import controller_base

STRING_1 = """
#include <ESP8266WiFi.h>
#include <list>
#include "./helpers/PinDefinition.h"
#include "./helpers/helpers.h"

using namespace std;
class ActuatorForEsp8266 : public Actuator
{
public:
  ActuatorForEsp8266(int pin, const string &identifier, const string &name) : Actuator(pin, identifier, name)
  {
    pinMode(this->pin, 1);
  };

public:
  void do_action() override
  {
    this->state = !this->state;
    digitalWrite(this->pin, this->state);
  }
};

//WebServer
const char *ssid = "Marcolino";
const char *password = "vmclvmclvmcl";
void webServer();

WiFiServer server(80);
"""

STRING_2 = """
ControlioBoaderController genericBoard = ControlioBoaderController(actuators);
void setup()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  pinMode(LED_BUILTIN, 1);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }
  genericBoard.setIP(WiFi.localIP().toString().c_str());
  """

SERVER = """
  presentYouSelf("http://192.168.1.10:5000", genericBoard.toJson().c_str());
  """

STRING_4 = """
  server.begin();
}

void loop()
{
  WiFiClient client = server.available();
  if (!client)
  {
    return;
  }
  while (!client.available())
  {
    delay(1);
  }
  String request = client.readStringUntil('\\r');
  client.print(genericBoard.main(request.c_str()).c_str());
  client.flush();
  return;
}
"""


class Esp8266Generator(FileGenerator):
    def generate_file_string(self):
        atuadores = 'list<Actuator *> actuators = { '
        for i in self.listOfActuators:
            atuadores += f'new ActuatorForEsp8266({i["pin"]}, "{i["identifier"]}", "{i["name"]}"),'
        atuadores += "};"
        print(atuadores)
        return controller_base + STRING_1 + atuadores + STRING_2 + SERVER + STRING_4
