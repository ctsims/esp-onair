#include "button.h"
#include "secrets.h"
#include "blinker.h"
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <WiFiUdp.h>
#include <time.h>
#include "net_helpers.h"
#include "periodic.h"

#define RECEIVE_PORT 9816

#define WAIT_INTERVAL 400

#define LED_PIN LED_BUILTIN
#define BUTTON_PIN D7
#define SWITCH_PIN D6

#define STATE_OFF 0
#define STATE_ON 1

#define SIGNAL_ON 1
#define SIGNAL_OFF 0
#define SIGNAL_CYCLE 2

LedBlinker Blink(LED_PIN);
ButtonController Buttons(BUTTON_PIN, -1, -1);

int panelState = STATE_OFF;

//helpers for processing received UDP messages
char packet[255];
bool fetched;
StaticJsonDocument<255> responseDoc;

WiFiClient net = WiFiClient();
WiFiUDP UDP;
IPAddress multicastIP(239,0,82,66);

void startListening() {
  // Begin listening to UDP port
  UDP.beginMulticast(WiFi.localIP(), multicastIP, RECEIVE_PORT);
  Serial.print("Listening on UDP port ");
  Serial.println(RECEIVE_PORT);
}

boolean udpRawReceive() {
  // If packet received...
  int packetSize = UDP.parsePacket();
  if (packetSize) {
    Serial.print("Received packet! Size: ");
    Serial.println(packetSize);
    int len = UDP.read(packet, 255);
    if (len > 0)
    {
      packet[len] = '\0';
    }
    Serial.print("Packet received from [");
    Serial.print(UDP.remoteIP());
    Serial.print("] ");
    Serial.println(packet);
    return true;
  }
  return false;
}

void processSignalMessage(IPAddress address, char packet[]) {
  deserializeJson(responseDoc, packet);
  int sig = responseDoc["signal"];

  switch (sig) {
    case SIGNAL_CYCLE:
      cyclePanelState();
      break;
    case SIGNAL_ON:
      if (panelState == STATE_OFF) {
        cyclePanelState();
      }
      break;
    case SIGNAL_OFF:
      if (panelState == STATE_ON) {
        cyclePanelState();
      }
      break;
    default:
      Serial.print("Unexpected signal code: ");
      Serial.println(sig);
      break;
  }
}

boolean udpReceive(void (*pFunc)(IPAddress address, char packet[])) {
  if (udpRawReceive()) {
    pFunc(UDP.remoteIP(), packet);
    return true;
  }
  return false;
}

void loop() {
  delay(100);
  Blink.loop();
  Buttons.loop();

  //Check for signals
  udpReceive(processSignalMessage);

  process_buttons();
}

void process_buttons() {
    switch (Buttons.current_event) {
    case EVENT_BUTTON_ONE:
      Serial.println("Manual Press");
      cyclePanelState();
      break;
    case EVENT_BUTTON_ONE_LONG:
      Serial.println("Long Press (unused)");
      break;
    default:
      break;
  }
}

void cyclePanelState() {
    if (panelState == STATE_OFF) {
      simulateInternalPress();
      panelState = STATE_ON;
    } else {
      simulateInternalPress();
      delay(WAIT_INTERVAL);
      simulateInternalPress();
      panelState = STATE_OFF;
    }
}


void simulateInternalPress() {
  Blink.ledON();
  digitalWrite(SWITCH_PIN, 0);
  delay(WAIT_INTERVAL);
  digitalWrite(SWITCH_PIN, 1);
  Blink.ledOFF();
}

void setup() {
  Serial.begin(115200);
  Buttons.setup();

  Blink.setup();
  delay(300);

  initWIFI();

  startListening();

  Blink.ledOFF();

  pinMode(SWITCH_PIN, OUTPUT);
  digitalWrite(SWITCH_PIN, 1);
}
