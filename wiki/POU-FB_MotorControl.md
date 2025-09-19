# FB_MotorControl

*Last updated: 2025-09-19 09:56:57*

## Overview

- **Type**: None
- **File**: `PLC/POUs/FB_MotorControl.TcPOU`

## Variables

| Name | Type | Default | Comment |
|------|------|---------|---------|
| `bEnable` | BOOL | - | Enable motor operation |
| `bStart` | BOOL | - | Start motor command |
| `bStop` | BOOL | - | Stop motor command |
| `bReset` | BOOL | - | Reset motor faults |
| `rSpeedSetpoint` | REAL | - | Speed setpoint (0.0 - 100.0 %) |
| `bMotorRunning` | BOOL | - | Motor is running |
| `bMotorFault` | BOOL | - | Motor fault condition |
| `bMotorReady` | BOOL | - | Motor ready for operation |
| `rActualSpeed` | REAL | - | Actual motor speed (%) |
| `rMotorCurrent` | REAL | - | Motor current (A) |
| `rMotorTorque` | REAL | - | Motor torque (%) |
| `bMotorRunning` | BOOL | - | Motor is running |
| `bMotorFault` | BOOL | - | Motor fault condition |
| `bMotorReady` | BOOL | - | Motor ready for operation |
| `rActualSpeed` | REAL | - | Actual motor speed (%) |
| `rMotorCurrent` | REAL | - | Motor current (A) |
| `rMotorTorque` | REAL | - | Motor torque (%) |
| `eMotorState` | E_MotorState | - | Timers and counters |
| `tonStartupDelay` | TON | - | Motor startup delay |
| `tonRampUp` | TON | - | Speed ramp up timer |
| `tonRampDown` | TON | - | Speed ramp down timer |
| `tonFaultTimer` | TON | - | Fault detection timer |
| `rSpeedCommand` | REAL | - | Internal speed command |
| `rSpeedFeedback` | REAL | - | Simulated speed feedback |
| `bStartEdge` | BOOL | - | Start command edge |
| `bLastStart` | BOOL | - | Previous start state |
| `bOvercurrent` | BOOL | - | Overcurrent fault |
| `bOverspeed` | BOOL | - | Overspeed fault |
| `bUnderspeed` | BOOL | - | Underspeed fault |
| `rMaxCurrent` | REAL | 15.0 | Maximum allowed current |
| `rMaxSpeed` | REAL | 105.0 | Maximum allowed speed |
| `rMinSpeed` | REAL | 5.0 | Minimum running speed |

## Implementation

```pascal
// =====================================================
// FB_MotorControl - Advanced Motor Control Function Block
// Purpose: Provide comprehensive motor control with diagnostics
// Author: Demo System
// Version: 1.1
// =====================================================

// Edge detection for start command
bStartEdge := bStart AND NOT bLastStart;
bLastStart := bStart;

// Input validation and limiting
IF rSpeedSetpoint > 100.0 THEN
	rSpeedSetpoint := 100.0;
ELSIF rSpeedSetpoint < 0.0 THEN
	rSpeedSetpoint := 0.0;
END_IF

// Main motor control state machine
CASE eMotorState OF
	E_MotorState.STOPPED:
		// Motor stopped - safe state
		bMotorRunning := FALSE;
		bMotorReady := bEnable AND NOT bMotorFault;
		rActualSpeed := 0.0;
		rMotorCurrent := 0.0;
		rMotorTorque := 0.0;
		rSpeedCommand := 0.0;
		
		// Reset timers
		tonStartupDelay(IN := FALSE);
		tonRampUp(IN := FALSE);
		tonRampDown(IN := FALSE);
		
		// Transition to starting
		IF bStartEdge AND bEnable AND NOT bMotorFault THEN
			eMotorState := E_MotorState.STARTING;
		END_IF
		
	E_MotorState.STARTING:
		// Motor startup sequence
		bMotorRunning := FALSE;
		bMotorReady := FALSE;
		
		// Startup delay
		tonStartupDelay(IN := TRUE, PT := T#1S);
		IF tonStartupDelay.Q THEN
			eMotorState := E_MotorState.RUNNING;
			tonRampUp(IN := TRUE, PT := T#3S);
		END_IF
		
		// Check for abort conditions
		IF bStop OR NOT bEnable OR bMotorFault THEN
			eMotorState := E_MotorState.STOPPING;
		END_IF
		
	E_MotorState.RUNNING:
		// Motor running - normal operation
		bMotorRunning := TRUE;
		bMotorReady := FALSE;
		
		// Speed ramping logic
		tonRampUp(IN := TRUE);
		IF tonRampUp.Q THEN
			// Ramp up complete - follow setpoint
			rSpeedCommand := rSpeedSetpoint;
		ELSE
			// Ramping up
			rSpeedCommand := rSpeedSetpoint * REAL_TO_TIME(tonRampUp.ET) / REAL_TO_TIME(tonRampUp.PT);
		END_IF
		
		// Simulate motor response (simplified)
		IF rSpeedFeedback < rSpeedCommand THEN
			rSpeedFeedback := rSpeedFeedback + 2.0; // Ramp up
		ELSIF rSpeedFeedback > rSpeedCommand THEN
			rSpeedFeedback := rSpeedFeedback - 2.0; // Ramp down
		END_IF
		
		// Limit feedback
		IF rSpeedFeedback < 0.0 THEN
			rSpeedFeedback := 0.0;
		ELSIF rSpeedFeedback > 100.0 THEN
			rSpeedFeedback := 100.0;
		END_IF
		
		rActualSpeed := rSpeedFeedback;
		
		// Simulate current and torque (simplified)
		rMotorCurrent := 2.0 + (rActualSpeed / 100.0) * 10.0;
		rMotorTorque := (rActualSpeed / 100.0) * 85.0;
		
		// Check for stop conditions or faults
		IF bStop OR NOT bEnable OR bMotorFault THEN
			eMotorState := E_MotorState.STOPPING;
		END_IF
		
	E_MotorState.STOPPING:
		// Motor stopping sequence
		bMotorRunning := FALSE;
		bMotorReady := FALSE;
		
		// Ramp down speed
		tonRampDown(IN := TRUE, PT := T#2S);
		IF tonRampDown.Q THEN
			rSpeedFeedback := 0.0;
			eMotorState := E_MotorState.STOPPED;
		ELSE
			rSpeedFeedback := rSpeedFeedback * (1.0 - REAL_TO_TIME(tonRampDown.ET) / REAL_TO_TIME(tonRampDown.PT));
		END_IF
		
		rActualSpeed := rSpeedFeedback;
		rMotorCurrent := rMotorCurrent * 0.9; // Decay current
		rMotorTorque := 0.0;
		
	E_MotorState.FAULT:
		// Motor fault state
		bMotorRunning := FALSE;
		bMotorReady := FALSE;
		bMotorFault := TRUE;
		rActualSpeed := 0.0;
		rMotorCurrent := 0.0;
		rMotorTorque := 0.0;
		rSpeedFeedback := 0.0;
		
		// Reset from fault
		IF bReset AND NOT (bOvercurrent OR bOverspeed OR bUnderspeed) THEN
			bMotorFault := FALSE;
			eMotorState := E_MotorState.STOPPED;
		END_IF
		
	ELSE
		// Invalid state - go to fault
		eMotorState := E_MotorState.FAULT;
		bMotorFault := TRUE;
END_CASE

// Fault detection logic
bOvercurrent := (rMotorCurrent > rMaxCurrent);
bOverspeed := (rActualSpeed > rMaxSpeed);
bUnderspeed := (rActualSpeed < rMinSpeed) AND bMotorRunning AND (rSpeedSetpoint > rMinSpeed);

// Fault timer - only trigger fault after sustained condition
tonFaultTimer(IN := (bOvercurrent OR bOverspeed OR bUnderspeed), PT := T#500MS);
IF tonFaultTimer.Q AND (eMotorState <> E_MotorState.FAULT) THEN
	eMotorState := E_MotorState.FAULT;
	bMotorFault := TRUE;
END_IF
```

## Additional Comments

- Basic motor control inputs
- Enable motor operation
- Start motor command
- Stop motor command
- Reset motor faults
- Speed setpoint (0.0 - 100.0 %)
- Motor status outputs
- Motor is running
- Motor fault condition
- Motor ready for operation
- Actual motor speed (%)
- Motor current (A)
- Motor torque (%)
- Internal state machine
- Timers and counters
- Motor startup delay
- Speed ramp up timer
- Speed ramp down timer
- Fault detection timer
- Internal variables
- Internal speed command
- Simulated speed feedback
- Start command edge
- Previous start state
- Fault detection
- Overcurrent fault
- Overspeed fault
- Underspeed fault
- Constants
- Maximum allowed current
- Maximum allowed speed
- Minimum running speed

---
*[Back to POUs Overview](POUs.md)*