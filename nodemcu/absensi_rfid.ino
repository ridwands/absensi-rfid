#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
     
const char* ssid     = "IniWifi";
const char* password = "lupaapatau";   
const char *host = "http://192.168.43.17:5000/mahasiswa"

int wifiStatus;
    

#define SS_PIN 4  //D2
#define RST_PIN 5 //D1

#include <SPI.h>
#include <MFRC522.h>

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
int statuss = 0;
int out = 0;
void setup() 
{
  Serial.begin(115200);   // Initiate a serial communication
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522

WiFi.begin(ssid, password);
 Serial.print("Your are connecting to ");
      Serial.print(ssid);
      
     
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
      Serial.println("");
      wifiStatus = WiFi.status();
      HTTPClient http;    //Declare object of class HTTPClient

if(wifiStatus == WL_CONNECTED){
//         Serial.println("");
         Serial.print("You Successfullu Connected To :!");  
         Serial.println(ssid);
         Serial.print("Your IP address is: ");
         Serial.println(WiFi.localIP());  
      }
      else{
        Serial.println("");
        Serial.println("WiFi not connected");
      }

    Serial.println("Please tag a card or keychain to see the UID !");
  Serial.println("");

  
}
void loop() 
{
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serial monitor
 // Serial.print(" UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
 //    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
   //  Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  Serial.println();

   HTTPClient http;    //Declare object of class HTTPClien
  
  http.begin(host);  
  http.addHeader("Content-Type", "application/json"); 

  StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
    JsonObject& JSONencoder = JSONbuffer.createObject(); 
 
    JSONencoder["rfid_id"] = content.substring(1);
    char JSONmessageBuffer[300];
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));

    int httpCode = http.POST(JSONmessageBuffer);

    String payload = http.getString();                                        //Get the response payload

    Serial.println(payload);    //Print request response payload
 
    http.end();  //Close connection
    delay(2000);
} 
