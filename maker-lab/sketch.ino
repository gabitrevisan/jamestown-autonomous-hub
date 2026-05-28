// ============================================================
// JAMESTOWN AUTONOMOUS HUB — Robotic Arm Controller v7.0
// Project-Based Maker Lab (PBML) — Global Solution FIAP 2026
// ============================================================

#include <Servo.h>

// --- Joystick BASE ---
const int J_BASE_X   = A0;
const int J_BASE_SEL = 2;

// --- Joystick LIFT ---
const int J_LIFT_X   = A1;
const int J_LIFT_SEL = 3;

// --- Joystick GRIP (Substituiu o Potenciômetro) ---
const int J_GRIP_X   = A2;

// --- Botão MODE e LED ---
const int BTN_MODE = 8;
const int PIN_LED  = 13;

// --- Servos ---
const int PIN_SERVO_LIFT = 9;
const int PIN_SERVO_GRIP = 10;
const int PIN_SERVO_BASE = 11;

// --- Limites ---
const int LIFT_MIN = 0;  const int LIFT_MAX = 180;
const int GRIP_MIN = 0;  const int GRIP_MAX = 180;
const int BASE_MIN = 0;  const int BASE_MAX = 180;
const int CENTER   = 90;

// --- Dead zone dos joysticks ---
const int JOY_DEAD_LOW  = 430;
const int JOY_DEAD_HIGH = 593;

// --- Modos de Velocidade ---
const int SPEED_STEP   = 3;  const int SPEED_DELAY   = 18;
const int PRECISE_STEP = 1;  const int PRECISE_DELAY = 30;
bool preciseMode = false;

// --- Posições Iniciais ---
int posBase = CENTER;
int posLift = 40;
int posGrip = 20;

// --- Throttle do terminal ---
const unsigned long PRINT_INTERVAL = 400;
unsigned long lastPrintTime = 0;
bool wasMoving = false;

// --- Debounce ---
bool lastSelBase = HIGH, lastSelLift = HIGH, lastBtnMode = HIGH;
unsigned long lastSelTime = 0;
const int SEL_DEBOUNCE = 250;

// --- Captura ---
int sampleCounter = 0;

// --- Servos ---
Servo servoLift;
Servo servoGrip;
Servo servoBase;

// --- Serial ---
String serialBuffer = "";

// ============================================================
// SETUP
// ============================================================
void setup() {
  Serial.begin(9600);

  pinMode(J_BASE_SEL, INPUT_PULLUP);
  pinMode(J_LIFT_SEL, INPUT_PULLUP);
  pinMode(BTN_MODE,   INPUT_PULLUP);
  pinMode(PIN_LED,    OUTPUT);

  servoLift.attach(PIN_SERVO_LIFT);
  servoGrip.attach(PIN_SERVO_GRIP);
  servoBase.attach(PIN_SERVO_BASE);

  applyPositions();
  printBanner();
  printDashboard();
}

// ============================================================
// LOOP
// ============================================================
void loop() {
  checkButtons();

  int step = preciseMode ? PRECISE_STEP  : SPEED_STEP;
  int spd  = preciseMode ? PRECISE_DELAY : SPEED_DELAY;

  bool moving = readJoysticks(step); // Agora todos os 3 eixos são lidos aqui

  if (moving) {
    applyPositions();
    digitalWrite(PIN_LED, HIGH);
    throttledPrint();
    delay(spd);
    wasMoving = true;
  } else {
    digitalWrite(PIN_LED, LOW);
    if (wasMoving) {
      printDashboard();
      wasMoving = false;
    }
  }

  readSerial();
  delay(10);
}

// ============================================================
// JOYSTICKS — BASE, LIFT e GRIP
// ============================================================
bool readJoysticks(int step) {
  bool moved = false;

  int jBase = analogRead(J_BASE_X);
  int jLift = analogRead(J_LIFT_X);
  int jGrip = analogRead(J_GRIP_X);

  if (jBase < JOY_DEAD_LOW)  { posBase = clamp(posBase - step, BASE_MIN, BASE_MAX); moved = true; }
  if (jBase > JOY_DEAD_HIGH) { posBase = clamp(posBase + step, BASE_MIN, BASE_MAX); moved = true; }

  // Push forward = subir
  if (jLift < JOY_DEAD_LOW)  { posLift = clamp(posLift + step, LIFT_MIN, LIFT_MAX); moved = true; }
  if (jLift > JOY_DEAD_HIGH) { posLift = clamp(posLift - step, LIFT_MIN, LIFT_MAX); moved = true; }

  // Esquerda/Direita = Abrir/Fechar garra
  if (jGrip < JOY_DEAD_LOW)  { posGrip = clamp(posGrip - step, GRIP_MIN, GRIP_MAX); moved = true; }
  if (jGrip > JOY_DEAD_HIGH) { posGrip = clamp(posGrip + step, GRIP_MIN, GRIP_MAX); moved = true; }

  return moved;
}

// ============================================================
// BOTÕES
// ============================================================
void checkButtons() {
  if (millis() - lastSelTime < SEL_DEBOUNCE) return;

  bool sBase = digitalRead(J_BASE_SEL);
  bool sLift = digitalRead(J_LIFT_SEL);
  bool sMode = digitalRead(BTN_MODE);

  // BASE SEL → reset ao centro
  if (sBase == LOW && lastSelBase == HIGH) {
    posBase = CENTER; posLift = CENTER; posGrip = CENTER;
    applyPositions();
    lastSelTime = millis();
    blinkLed(3);
    printEvent("RESET — todos os servos ao centro (90 graus)");
    printDashboard();
  }

  // LIFT SEL → capturar amostra
  if (sLift == LOW && lastSelLift == HIGH) {
    lastSelTime = millis();
    triggerCapture();
  }

  // BTN MODE → Speed ↔ Precise (Afeta todos os 3 eixos)
  if (sMode == LOW && lastBtnMode == HIGH) {
    preciseMode = !preciseMode;
    lastSelTime = millis();
    blinkLed(preciseMode ? 2 : 1);
    printEvent(preciseMode
      ? "MODO: PRECISE [1 grau/passo ]"
      : "MODO: SPEED   [3 graus/passo]");
    printDashboard();
  }

  lastSelBase = sBase;
  lastSelLift = sLift;
  lastBtnMode = sMode;
}

// ============================================================
// APLICA POSIÇÕES
// ============================================================
void applyPositions() {
  servoBase.write(posBase);
  servoLift.write(posLift);
  servoGrip.write(posGrip);
}

// ============================================================
// THROTTLE DO PRINT
// ============================================================
void throttledPrint() {
  if (millis() - lastPrintTime >= PRINT_INTERVAL) {
    printDashboard();
  }
}

// ============================================================
// DASHBOARD
// ============================================================
void printDashboard() {
  Serial.println(F("\n  ================================"));
  Serial.println(F("   JAMESTOWN ARM — STATUS"));
  Serial.println(F("  ================================"));
  printBar("BASE ", posBase, BASE_MAX);
  printBar("LIFT ", posLift, LIFT_MAX);
  printBar("GRIP ", posGrip, GRIP_MAX);
  Serial.println(F("  --------------------------------"));
  Serial.print(F("   MODO GLOBAL : "));
  Serial.println(preciseMode ? F("PRECISE  [1 grau /passo]") : F("SPEED    [3 graus/passo]"));
  Serial.print(F("   AMOSTRAS    : "));
  Serial.println(sampleCounter);
  Serial.println(F("  ================================\n"));

  lastPrintTime = millis();
}

void printBar(String label, int value, int maxVal) {
  const int W = 18;
  int filled  = map(value, 0, maxVal, 0, W);

  String bar = "  " + label + "[";
  for (int i = 0; i < W; i++) bar += (i < filled) ? "=" : " ";
  bar += "] ";

  String deg = String(value);
  while ((int)deg.length() < 3) deg = " " + deg;
  bar += deg + " graus";

  Serial.println(bar);
}

// ============================================================
// CAPTURA
// ============================================================
void triggerCapture() {
  sampleCounter++;
  blinkLed(3);
  Serial.println(F("\n  +------------------------------+"));
  Serial.println(F("  |    >>> AMOSTRA CAPTURADA    |"));
  Serial.println(F("  +------------------------------+"));
  Serial.println("  sample_id  : JAM-GH01-SMP-" + zeroPad(sampleCounter, 3));
  Serial.println("  base       : " + String(posBase) + " graus");
  Serial.println("  lift       : " + String(posLift) + " graus");
  Serial.println("  grip       : " + String(posGrip) + " graus");
  Serial.println(F("  status     : SAMPLE_COLLECTED"));
  Serial.println(F("  source     : PBML_ARM_v7"));
  Serial.println(F("  +------------------------------+\n"));
}

// ============================================================
// SERIAL
// ============================================================
void readSerial() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (serialBuffer.length() > 0) {
        processSerial(serialBuffer);
        serialBuffer = "";
      }
    } else {
      serialBuffer += c;
    }
  }
}

void processSerial(String cmd) {
  cmd.trim();
  cmd.toUpperCase();
  if (cmd.length() == 0) return;

  if (cmd == "STATUS") { printDashboard(); return; }
  if (cmd == "MODE")   { printEvent(preciseMode ? "PRECISE" : "SPEED"); return; }
  if (cmd == "RESET")  {
    posBase = CENTER; posLift = CENTER; posGrip = CENTER;
    applyPositions();
    printEvent("RESET todos os eixos ao centro");
    printDashboard();
    return;
  }

  char letter   = cmd.charAt(0);
  bool hasAngle = cmd.length() > 1 && isDigit(cmd.charAt(1));
  int  angle    = hasAngle ? cmd.substring(1).toInt() : -1;
  int  step     = preciseMode ? 1 : 5;

  switch (letter) {
    case 'U': posLift = hasAngle ? clamp(angle, LIFT_MIN, LIFT_MAX) : clamp(posLift + step, LIFT_MIN, LIFT_MAX); break;
    case 'D': posLift = hasAngle ? clamp(angle, LIFT_MIN, LIFT_MAX) : clamp(posLift - step, LIFT_MIN, LIFT_MAX); break;
    case 'O': posGrip = hasAngle ? clamp(angle, GRIP_MIN, GRIP_MAX) : clamp(posGrip - step, GRIP_MIN, GRIP_MAX); break;
    case 'C': posGrip = hasAngle ? clamp(angle, GRIP_MIN, GRIP_MAX) : clamp(posGrip + step, GRIP_MIN, GRIP_MAX); break;
    case 'L': posBase = hasAngle ? clamp(angle, BASE_MIN, BASE_MAX) : clamp(posBase - step, BASE_MIN, BASE_MAX); break;
    case 'R': posBase = hasAngle ? clamp(angle, BASE_MIN, BASE_MAX) : clamp(posBase + step, BASE_MIN, BASE_MAX); break;
    default:  printEvent("Invalido: " + cmd); return;
  }

  applyPositions();
  printDashboard();
}

// ============================================================
// UTILITÁRIOS
// ============================================================
int clamp(int v, int mn, int mx) { return max(mn, min(mx, v)); }

void blinkLed(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(PIN_LED, HIGH); delay(100);
    digitalWrite(PIN_LED, LOW);  delay(100);
  }
}

void printEvent(String msg) { Serial.println("  >> " + msg); }

String zeroPad(int v, int w) {
  String s = String(v);
  while ((int)s.length() < w) s = "0" + s;
  return s;
}

void printBanner() {
  Serial.println(F("\n  ================================"));
  Serial.println(F("   JAMESTOWN AUTONOMOUS HUB"));
  Serial.println(F("   Robotic Arm Controller v7.1"));
  Serial.println(F("   PBML — Global Solution 2026"));
  Serial.println(F("  ================================"));
  Serial.println(F("   J1 (BASE) SEL  → reset ao centro"));
  Serial.println(F("   J2 (LIFT) SEL  → capturar amostra"));
  Serial.println(F("   J3 (GRIP) HORZ → abrir/fechar"));
  Serial.println(F("   BTN MODE       → Speed / Precise"));
  Serial.println(F("  ================================\n"));
}