# FB_ConveyorControl

*Last updated: 2025-09-19 07:05:35*

## Overview

- **Type**: None
- **File**: `PLC/POUs/FB_ConveyorControl.TcPOU`

## Variables

| Name | Type | Default | Comment |
|------|------|---------|---------|
| `bStart` | BOOL | - | Start conveyor command |
| `bReset` | BOOL | - | Reset faults and errors |
| `nSpeed` | INT | - | Desired speed percentage (0-100) |
| `bRunning` | BOOL | - | Conveyor is running |
| `bFault` | BOOL | - | Fault condition present |
| `bReady` | BOOL | - | Ready to start |
| `nActualSpeed` | INT | - | Actual speed percentage |
| `bRunning` | BOOL | - | Conveyor is running |
| `bFault` | BOOL | - | Fault condition present |
| `bReady` | BOOL | - | Ready to start |
| `nActualSpeed` | INT | - | Actual speed percentage |
| `eState` | E_MotorState | - | Current motor state |
| `stConveyorData` | ST_ConveyorData | - | Conveyor configuration data |
| `tonStartDelay` | TON | - | Start delay timer |
| `tonRunTime` | TON | - | Running time counter |
| `tonFaultDelay` | TON | - | Fault detection delay |
| `bInternalFault` | BOOL | - | Internal fault flag |
| `bStartRequest` | BOOL | - | Start request edge detection |
| `bLastStart` | BOOL | - | Previous start signal |
| `nStartCount` | UDINT | - | Number of starts |
| `nRunTimeHours` | UDINT | - | Running time in hours |

## Implementation

```pascal
// =====================================================
// FB_ConveyorControl - Conveyor Control Function Block
// Purpose: Control conveyor motor with safety features
// Author: Demo System  
// Version: 1.0
// =====================================================

// Edge detection for start command
bStartRequest := bStart AND NOT bLastStart;
bLastStart := bStart;

// Count start requests
IF bStartRequest THEN
	nStartCount := nStartCount + 1;
END_IF

// Reset logic
IF NOT bReset THEN
	bInternalFault := FALSE;
	eState := E_MotorState.STOPPED;
END_IF

// Main state machine
CASE eState OF
	E_MotorState.STOPPED:
		// Conveyor stopped state
		bRunning := FALSE;
		bReady := TRUE;
		nActualSpeed := 0;
		
		// Check for start condition
		IF bStart AND bReset AND NOT bInternalFault THEN
			eState := E_MotorState.STARTING;
			tonStartDelay(IN := TRUE, PT := T#2S);
		END_IF
		
	E_MotorState.STARTING:
		// Starting sequence
		bRunning := FALSE;
		bReady := FALSE;
		
		tonStartDelay(IN := TRUE);
		IF tonStartDelay.Q THEN
			eState := E_MotorState.RUNNING;
			tonStartDelay(IN := FALSE);
			tonRunTime(IN := TRUE);
		END_IF
		
		// Check for abort conditions
		IF NOT bStart OR NOT bReset THEN
			eState := E_MotorState.STOPPING;
		END_IF
		
	E_MotorState.RUNNING:
		// Normal running state
		bRunning := TRUE;
		bReady := FALSE;
		
		// Speed control (simplified)
		IF nSpeed > 100 THEN
			nActualSpeed := 100;
		ELSIF nSpeed < 0 THEN
			nActualSpeed := 0;
		ELSE
			nActualSpeed := nSpeed;
		END_IF
		
		// Running time counter
		tonRunTime(IN := TRUE);
		
		// Check for stop conditions
		IF NOT bStart OR NOT bReset OR bInternalFault THEN
			eState := E_MotorState.STOPPING;
		END_IF
		
	E_MotorState.STOPPING:
		// Stopping sequence
		bRunning := FALSE;
		bReady := FALSE;
		nActualSpeed := 0;
		
		tonRunTime(IN := FALSE);
		eState := E_MotorState.STOPPED;
		
	E_MotorState.FAULT:
		// Fault state
		bRunning := FALSE;
		bReady := FALSE;
		bFault := TRUE;
		nActualSpeed := 0;
		
		// Reset from fault
		IF bReset THEN
			eState := E_MotorState.STOPPED;
			bFault := FALSE;
		END_IF
		
	ELSE
		// Invalid state - go to fault
		eState := E_MotorState.FAULT;
		bInternalFault := TRUE;
END_CASE

// Fault detection logic
tonFaultDelay(IN := (nActualSpeed > 95 AND bRunning), PT := T#30S);
IF tonFaultDelay.Q THEN
	bInternalFault := TRUE;
	eState := E_MotorState.FAULT;
END_IF

// Update conveyor data structure
stConveyorData.bRunning := bRunning;
stConveyorData.nSpeed := nActualSpeed;
stConveyorData.nStartCount := nStartCount;
stConveyorData.tRunTime := UDINT_TO_TIME(tonRunTime.ET);
```

## Additional Comments

- Control inputs
- Start conveyor command
- Reset faults and errors
- Desired speed percentage (0-100)
- Status outputs
- Conveyor is running
- Fault condition present
- Ready to start
- Actual speed percentage
- Internal variables
- Current motor state
- Conveyor configuration data
- Timers
- Start delay timer
- Running time counter
- Fault detection delay
- Internal flags
- Internal fault flag
- Start request edge detection
- Previous start signal
- Counters
- Number of starts
- Running time in hours

---
*[Back to POUs Overview](POUs.md)*