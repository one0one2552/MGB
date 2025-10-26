# Relay Level Shifter - 3.3V zu 5V

## Problem

Raspberry Pi GPIO gibt **3.3V** bei HIGH aus, aber dein Relay-Modul braucht **5V** um sicher zu schalten.

## Lösung 1: Logic Level Converter (Einfach)

Kaufe einen **Bi-Directional Logic Level Converter** (z.B. von Adafruit, SparkFun).

**Anschluss:**
```
Raspberry Pi          Level Converter          Relay-Modul
├─ 3.3V    ────────►  LV (Low Voltage)
├─ GPIO 27 ────────►  LV1                HV1 ──► Signal
└─ GND     ────────►  GND                GND ──► GND
                      
Netzteil 5V ────────►  HV (High Voltage)
                      (oder vom Relay VCC abzweigen)
```

**Kosten:** ~3-5 EUR

---

## Lösung 2: NPN Transistor als Schalter (DIY)

**Bauteile:**
- 1x NPN Transistor (BC547, 2N2222, oder ähnlich)
- 1x 1kΩ Widerstand (für Basis)
- 1x 10kΩ Widerstand (Pull-Up, optional)

**Schaltplan:**
```
Raspberry Pi GPIO 27
       │
       └─── 1kΩ ───┬─ Basis (B)
                   │
             NPN Transistor
                   │
       ┌───────────┴─ Kollektor (C)
       │              │
       │           Relay Signal Pin
       │              │
       └──── 5V ──────┘ (über 10kΩ Pull-Up)
       
     Emitter (E) ─── GND
```

**Funktionsweise:**
- GPIO HIGH (3.3V) → Transistor leitet → Kollektor zieht auf GND → Relay Signal LOW (0V) → Relay AN
- GPIO LOW (0V) → Transistor sperrt → Kollektor auf 5V (Pull-Up) → Relay Signal HIGH (5V) → Relay AUS

**Code-Anpassung:**
In `config.yaml` setze:
```yaml
heater:
  inverted: true  # Weil Transistor invertiert!
```

---

## Lösung 3: Open-Drain/Open-Collector Setup

Wenn dein Relay-Modul einen Pull-Up Widerstand hat:

**Anschluss:**
```
Raspberry Pi GPIO 27 ──► Relay Signal
Relay VCC ──────────────► 5V Netzteil
Relay GND ──────────────► GND (gemeinsam mit Pi)
```

**Code-Anpassung:**
GPIO als Open-Drain verwenden (LOW = GND, HIGH = floating/high-impedance)

---

## Test welche Lösung du brauchst

1. **Messe mit Multimeter:**
   - GPIO 27 bei HIGH: Sollte 3.3V sein
   - Relay Signal-Eingang: Welche Spannung braucht es?

2. **Prüfe Relay-Modul Datenblatt:**
   - Signal Input Voltage: 3.3V oder 5V?
   - Logic Level: TTL oder CMOS?

3. **Teste mit 5V direkt:**
   - Verbinde Relay Signal mit 5V → Relay sollte AN sein
   - Verbinde Relay Signal mit GND → Relay sollte AUS sein

---

## Empfehlung

Für **dein Setup** (3.3V GPIO reicht nicht):

**→ Verwende einen NPN Transistor (Lösung 2)**

Das ist die einfachste und billigste Lösung ohne zusätzliche Module.

**Alternative:** Kaufe ein **3.3V kompatibles Relay-Modul** das direkt mit Raspberry Pi GPIO funktioniert.
