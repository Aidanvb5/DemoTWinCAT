# MAIN

*Last updated: 2025-09-19 07:05:35*

## Overview

- **Type**: None
- **File**: `PLC/POUs/MAIN.TcPOU`
- **Author**: Demo System
- **Date**: 2024

## Variables

| Name | Type | Default | Comment |
|------|------|---------|---------|
| `Author` | Demo System
	// Date | - | - |
| `fbConveyor1` | FB_ConveyorControl | - | - |
| `fbConveyor2` | FB_ConveyorControl | - | System control variables |
| `bSystemEnable` | BOOL | FALSE | - |
| `bEmergencyStop` | BOOL | FALSE | - |
| `bAutoMode` | BOOL | TRUE | Status monitoring |
| `nSystemState` | INT | 0 | - |
| `sStatusMessage` | STRING(255) | 'System Initialized' | Cycle counter for demo purposes |
| `nCycleCounter` | UDINT | 0 | Timer for auto mode cycling |
| `tonAutoTimer` | TON | - | - |

## Implementation

```pascal
// =====================================================
// MAIN Program - Demo TwinCAT Application  
// Purpose: Demonstrate GitHub integration with TwinCAT3
// =====================================================

// Increment cycle counter
nCycleCounter := nCycleCounter + 1;

// Auto timer for demonstration
tonAutoTimer(IN := bAutoMode, PT := T#5S);

// System state machine
CASE nSystemState OF
	0: // Initialize
		sStatusMessage := 'System Initializing...';
		IF NOT bEmergencyStop THEN
			nSystemState := 10;
		END_IF
		
	10: // Ready
		sStatusMessage := 'System Ready';
		IF bSystemEnable AND NOT bEmergencyStop THEN
			nSystemState := 20;
		END_IF
		
	20: // Running
		sStatusMessage := 'System Running';
		
		// Auto mode demonstration
		IF bAutoMode AND tonAutoTimer.Q THEN
			fbConveyor1.bStart := NOT fbConveyor1.bStart;
			fbConveyor2.bStart := NOT fbConveyor2.bStart;
			tonAutoTimer(IN := FALSE);
		END_IF
		
		// Check for stop conditions
		IF bEmergencyStop OR NOT bSystemEnable THEN
			nSystemState := 30;
		END_IF
		
	30: // Stopping
		sStatusMessage := 'System Stopping...';
		fbConveyor1.bStart := FALSE;
		fbConveyor2.bStart := FALSE;
		nSystemState := 10;
		
	ELSE
		nSystemState := 0;
END_CASE

// Call conveyor control function blocks
fbConveyor1(
	bStart := fbConveyor1.bStart,
	bReset := NOT bEmergencyStop,
	nSpeed := 75
);

fbConveyor2(
	bStart := fbConveyor2.bStart,
	bReset := NOT bEmergencyStop,
	nSpeed := 50
);

// Update global variables
GVL_System.bSystemRunning := (nSystemState = 20);
GVL_System.nCycleCount := nCycleCounter;
GVL_System.sSystemStatus := sStatusMessage;
```

## Additional Comments

- Demo Application Main Program
- This program demonstrates a simple conveyor control system
- Author: Demo System
- Date: 2024
- Conveyor control instances
- System control variables
- Status monitoring
- Cycle counter for demo purposes
- Timer for auto mode cycling

---
*[Back to POUs Overview](POUs.md)*