# 🤖 Smart Vacuum Prolog Planner

A **modular desktop application** built with **Python**, **CustomTkinter**, and **SWI-Prolog** (via **PySwip**) that simulates a smart robotic vacuum cleaner.

The robot can plan routes, clean rooms, return to its dock, and respond to dynamic noise (dirt). All reasoning is powered by a small Prolog knowledge base.

---

## ✨ Features

* 🧠 **Prolog-based reasoning** – paths, room states, and cleaning rules are defined in Prolog.
* 🗺️ **Interactive map** – visual canvas showing rooms, connections, the robot, and dirt particles.
* 🧹 **Manual controls** – move the robot, clean rooms, add noise, dock, and reset the environment.
* 🔍 **Query interface** – type custom Prolog queries and see results in real time.
* 📜 **Execution tracing** – every Prolog call, exit, rule, and failure is logged with timestamps.
* 🎨 **Animations** – smooth robot movement, cleaning sparkles, and docking/charging effects.
* 🧩 **Modular architecture** – clean separation of concerns (GUI, state, logic, drawing, trace).

---

## 📋 Prerequisites

* **Python 3.8+**
* **SWI-Prolog** installed on your system
* **pip packages**

  * `customtkinter`
  * `pyswip`

---

## 📦 Installation

### 1. Clone or Download the Project

Download or clone the repository to your local machine.

### 2. Install SWI-Prolog

Download and install SWI-Prolog from:

https://www.swi-prolog.org/Download.html

Make sure it is available in your system PATH:

```bash
swipl --version
```

### 3. Install Python Dependencies

```bash
pip install customtkinter pyswip
```

### 4. Verify Prolog Connection (Optional)

```python
from pyswip import Prolog

prolog = Prolog()
print(list(prolog.query("member(X, [a,b,c])")))
```

Expected output:

```python
[{'X': 'a'}, {'X': 'b'}, {'X': 'c'}]
```

---

## 🚀 Usage

Run the application:

```bash
python main.py
```

### Main Window Layout

#### Left Panel

* Interactive map canvas
* Manual control buttons

#### Right Panel

* Prolog query input
* Preset query buttons
* Find-and-Execute Plan button
* Execution trace output

---

## ⚡ Quick Start

### Clean the Bedroom

Click:

```text
🧹 Clean Bedroom
```

The robot moves to the bedroom and cleans it.

### Dock and Charge

Click:

```text
⚡ Dock (Charge)
```

The robot returns to the dock and displays a charging animation.

### Make a Room Dirty

Click:

```text
🌊 Bedroom Noise
```

The room becomes dirty again.

### Reset Environment

Click:

```text
🔄 Default State
```

All rooms return to a clean state.

### Automatic Planning

Click:

```text
🔍 Find and Execute Plan
```

The robot automatically:

1. Moves to the bedroom
2. Cleans the bedroom
3. Returns to the dock

### Execute Custom Prolog Queries

Example:

```prolog
can_move(dock, hall)
```

Press **Run** to execute.

---

## 🧩 Module Structure

| Module           | Responsibility                                                    |
| ---------------- | ----------------------------------------------------------------- |
| `config.py`      | Room coordinates, sizes, color utilities, and appearance settings |
| `prolog_init.py` | Prolog engine setup, facts and rules                              |
| `state.py`       | Global state management and noise generation                      |
| `trace.py`       | Trace logging functions                                           |
| `drawing.py`     | Canvas rendering and animations                                   |
| `actions.py`     | Robot actions (move, clean, dock, noise)                          |
| `queries.py`     | Query execution and planning                                      |
| `main.py`        | GUI creation and application entry point                          |

---

## 📁 File Structure

```text
vacuum_cleaner/
│
├── main.py
├── config.py
├── prolog_init.py
├── state.py
├── trace.py
├── drawing.py
├── actions.py
├── queries.py
├── README.md
```

---

## 🧪 Example Prolog Queries

### List All Rooms

```prolog
room(X)
```

### Check Movement

```prolog
can_move(dock, bedroom)
```

### Check Cleaning Permission

```prolog
can_clean(bedroom)
```

### Show Connections

```prolog
connected(X, Y)
```

---

## 🛠️ Customization

### Map Layout

Modify:

```python
room_coords
room_sizes
```

and update connection facts in:

```text
prolog_init.py
```

### Noise Density

Adjust:

```python
generate_noise_for_room()
```

inside:

```text
state.py
```

### Colors and Theme

Update color values in:

```text
drawing.py
```

---

## 📄 License

This project is released under the **MIT License**.

You are free to:

* Use
* Modify
* Distribute
* Extend

the project for personal or commercial purposes.

---

## ❤️ Acknowledgements

* **CustomTkinter** — Modern Tkinter-based UI framework
* **PySwip** — Python ↔ Prolog bridge
* **SWI-Prolog** — Logic programming engine powering the planner
