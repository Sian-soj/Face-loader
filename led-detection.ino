int redPin = 13; // distracte
int ldrPin = A0; // dark and light
int threshold = 700;
int greenpin = 12; // focused

void setup()
{
  pinMode(redPin, OUTPUT);
  pinMode(greenpin, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  // --- 1. LDR check & send status ---
  int ldrValue = analogRead(ldrPin);

  if (ldrValue > threshold)
  {
    Serial.println("DARK"); // Lights OFF
  }
  else
  {
    Serial.println("LIGHT"); // Lights ON
  }

  // --- 2. Check if Python sent LED control command ---
  if (Serial.available())
  {
    char data = Serial.read();
    if (data == '1')
    {
      digitalWrite(redPin, HIGH);
      digitalWrite(greenpin, LOW); // Focused → LED OFF
    }
    else if (data == '0')
    {
      digitalWrite(redPin, LOW);
      digitalWrite(greenpin, HIGH); // Distracted → LED ON
    }
  }

  delay(100); // Small delay to avoid spam
}