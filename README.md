# 📟 MaxScope

A desktop oscilloscope monitoring application built with **Python**, **tkinter**, and **PyVISA**.  
MaxScope connects to a Tektronix oscilloscope over TCP/IP, reads waveform data from **Channel 3** and **Channel 4**, displays live peak measurements, and logs measurement history in a clean Windows-style interface.

---

## Overview

MaxScope is designed for real-time monitoring of oscilloscope data in a simple desktop environment. It continuously acquires waveform samples, scales them using the oscilloscope preamble, detects the peak current on **CH4**, and displays the corresponding voltage from **CH3** at the same time index.

The software also records measurement history, allows selective clearing of entries, and supports export to CSV for later analysis.

---

## ✨ Features

- Live connection to a **Tektronix oscilloscope** using **PyVISA**
- Continuous waveform acquisition over **TCP/IP**
- Real-time display of:
  - **Channel 4 peak current**
  - **Corresponding Channel 3 voltage**
- Automatic waveform scaling using oscilloscope preamble parameters
- Measurement history table with:
  - alternating row styling
  - live count tracking
  - right-click context menu
- Export logged data to **CSV**
- Clear:
  - selected measurements
  - full history
- Classic Windows-style GUI with a clean engineering-focused layout
- Connection status indicator with visual feedback

---

## 🛠 Tech Stack

- **Python**
- **tkinter** for GUI
- **PyVISA** for oscilloscope communication
- **NumPy** for waveform processing
- **CSV / datetime** for data export and logging

---

## How It Works

1. The application connects to the oscilloscope using a VISA TCP/IP resource string.
2. Acquisition settings are configured automatically.
3. Waveforms are read from:
   - **CH3**
   - **CH4**
4. The software:
   - finds the peak value in **CH4**
   - locates the same index in **CH3**
   - displays both values in the main interface
5. If either value changes significantly, the reading is stored in the history table.
6. The user can export the logged data to CSV.

---

## 📡 Instrument Connection

The program uses **PyVISA** to connect to an oscilloscope with a resource string like:

```python
TCPIP0::10.200.22.14::INSTR
