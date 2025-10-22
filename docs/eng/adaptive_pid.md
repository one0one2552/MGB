# Adaptive PID Control - Documentation

## Overview

The MGB - Mushroom Grow Box uses an **adaptive PID control** that automatically adjusts to the system dynamics. You no longer need to manually tune the parameters via the YAML file!

## What is PID Control?

A PID controller consists of three components:

- **P (Proportional)**: Reacts proportionally to the current error
- **I (Integral)**: Eliminates steady-state errors over time
- **D (Derivative)**: Dampens overshoot and oscillations

## Adaptive vs. Manual Control

### 🌟 Adaptive Control (RECOMMENDED)

**Advantages:**
- ✅ Automatically adapts
- ✅ Learns optimal parameters itself
- ✅ No manual tuning required
- ✅ Works even with changing conditions
- ✅ Ideal for beginners

**How it works:**
1. The controller starts with the base parameters from config.yaml
2. Every 10 measurement cycles it analyzes the performance:
   - Average error
   - Error variance (oscillation)
   - Steady-state error
3. Based on the analysis it adjusts the parameters:
   - On oscillation: Reduces Kp, increases Kd
   - On large error: Increases Kp
   - On steady-state error: Increases Ki
4. Parameters are limited to reasonable ranges (0.1x - 5x of base values)

### ⚙️ Manual Control

**When useful:**
- You have experience with PID control
- You want very specific parameters
- The system behaves very unusually

**Disadvantages:**
- ❌ Requires expert knowledge
- ❌ Time-consuming (trial-and-error)
- ❌ Must be readjusted when changes occur

## Configuration via Web Interface

### Activate Adaptive Control (Default)

1. Open **Settings** in the web interface
2. Scroll to the **"🎛️ PID Control"** section
3. Enable the checkbox **"Enable Adaptive PID Control"**
4. Save the settings

✨ **Done!** The system now learns automatically.

### Set Manual Parameters

1. Open **Settings** in the web interface
2. Scroll to the **"🎛️ PID Control"** section
3. Disable the checkbox **"Enable Adaptive PID Control"**
4. The manual PID parameters become visible
5. Adjust Kp, Ki, Kd for each controller (temperature, humidity, CO₂)
6. Save the settings

## Parameter Tuning (manual control only)

### General Guidelines

**Kp (Proportional Gain):**
- Too small → Slow response
- Too large → Overshoot, oscillation
- Recommended: 1.0 - 3.0

**Ki (Integral Gain):**
- Too small → Steady-state error remains
- Too large → Slow oscillation
- Recommended: 0.1 - 1.0

**Kd (Derivative Gain):**
- Too small → Overshoot
- Too large → Sensitive to noise
- Recommended: 0.3 - 2.0

### Ziegler-Nichols Method

1. Set Ki = 0, Kd = 0
2. Increase Kp gradually until the system oscillates
3. Note Kp_critical and oscillation period T
4. Calculate optimal parameters:
   - Kp = 0.6 × Kp_critical
   - Ki = 1.2 × Kp_critical / T
   - Kd = 0.075 × Kp_critical × T

## Recommended Starting Values

### Temperature Controller
```yaml
kp: 2.0   # Moderate response
ki: 0.5   # Medium integral action
kd: 1.0   # Damping
```

### Humidity Controller
```yaml
kp: 1.5   # Slightly weaker response (sluggish system)
ki: 0.3   # Low integral action
kd: 0.5   # Light damping
```

### CO₂ Controller
```yaml
kp: 1.0   # Moderate response
ki: 0.2   # Low integral action
kd: 0.3   # Light damping
```

## Diagnosing Control Problems

### Problem: System oscillates (swings back and forth)

**Symptom:** Temperature/humidity fluctuates strongly around the setpoint

**Solution with manual control:**
1. Reduce Kp by 20-30%
2. Increase Kd by 20-30%

**With adaptive control:** 
- Automatically detected and corrected
- System should stabilize after 2-3 hours

### Problem: System doesn't reach setpoint

**Symptom:** Constant distance to setpoint remains

**Solution with manual control:**
1. Increase Ki by 20-30%

**With adaptive control:**
- Automatically detected and corrected
- Error should disappear after 1-2 hours

### Problem: System responds too slowly

**Symptom:** Takes very long to reach setpoint

**Solution with manual control:**
1. Increase Kp by 20-30%

**With adaptive control:**
- Automatically detected and corrected
- Response should be faster after 1 hour

### Problem: Overshooting

**Symptom:** System shoots past the setpoint

**Solution with manual control:**
1. Increase Kd by 30-50%
2. Reduce Kp by 10-20%

**With adaptive control:**
- Automatically detected and corrected

## API Access

### Get Current Tuning Status

The PID controller objects offer a `get_tuning_info()` method:

```python
from controllers.pid_controller import PIDController

# Create controller
pid = PIDController(kp=2.0, ki=0.5, kd=1.0, adaptive=True)

# After some updates...
info = pid.get_tuning_info()
print(info)
# {
#     'kp': 2.15,        # Current Kp (was adjusted)
#     'ki': 0.48,        # Current Ki
#     'kd': 1.23,        # Current Kd
#     'kp_base': 2.0,    # Base Kp
#     'ki_base': 0.5,    # Base Ki
#     'kd_base': 1.0,    # Base Kd
#     'adaptive': True,
#     'avg_error': 0.3,  # Average error
#     'error_count': 20
# }
```

### Toggle Adaptive Control Programmatically

```python
# Disable adaptive control
pid.set_adaptive(False)  # Uses base parameters again

# Enable adaptive control
pid.set_adaptive(True)   # Starts adaptive adjustment

# Reset to base parameters
pid.reset_to_base_parameters()
```

## Best Practices

### ✅ DO's

- Use adaptive control as default
- Give the system 2-4 hours to learn
- Monitor performance in the dashboard
- Use the base parameters as a good starting point

### ❌ DON'Ts

- Don't switch between adaptive/manual too often
- Don't change PID parameters manually daily
- Don't use extreme values (e.g., Kp > 10)
- Don't set Ki too high (leads to instability)

## Technical Details

### Adaptation Algorithm

```python
# Every 10 measurements:
if oscillating:
    kp *= 0.99  # 1% reduction
    kd *= 1.01  # 1% increase
elif large_error:
    kp *= 1.02  # 2% increase
elif steady_state_error:
    ki *= 1.01  # 1% increase

# Limiting
kp = clamp(kp, kp_base * 0.1, kp_base * 5.0)
ki = clamp(ki, ki_base * 0.1, ki_base * 5.0)
kd = clamp(kd, kd_base * 0.1, kd_base * 5.0)
```

### Learning Rate

The learning rate determines how fast the parameters change:
- Default: 0.01 (1% per adjustment)
- Faster: 0.05 (5% per adjustment) - can become unstable
- Slower: 0.005 (0.5% per adjustment) - very stable, but slow

## Summary

The **adaptive PID control** is the recommended solution for most users:

- ✨ No manual adjustment required
- 🧠 Automatically learns optimal parameters
- 🔄 Adapts to changing conditions
- 📊 Continuously improves

Only experts should use manual control when very specific requirements exist or the adaptive system doesn't work in exceptional cases.
