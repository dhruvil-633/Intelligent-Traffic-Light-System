


# Intelligent Traffic Light System with Emergency Vehicle Priority

**Research Paper:** \[[https://www.ijraset.com/best-journal/a-novel-approach-for-improved-traffic-management-for-emergency-service-vehicles](https://doi.org/10.22214/ijraset.2025.73349)]

## Overview

This project simulates an intelligent traffic light system designed to optimize traffic flow at a four-way intersection while prioritizing emergency vehicles such as ambulances and fire trucks.

Using a **mathematical time-sequence algorithm** for signal timing and a **pygame-based simulation**, the system dynamically controls traffic lights and vehicle movement. It detects emergency vehicle arrivals and temporarily overrides normal signal cycles to clear their path efficiently, enhancing emergency response times and reducing traffic congestion.

---



## Features

* **Four-way traffic light simulation** with configurable green, yellow, and red signal durations.
* **Dynamic vehicle generation**, including cars, buses, trucks, bikes, ambulances, and fire trucks.
* **Emergency vehicle priority handling:** When an emergency vehicle appears, the system turns all traffic signals blue temporarily, then gives green light priority to the emergency vehicle's direction.
* **Vehicle movement and lane management** using pygame sprites with realistic speed and stopping behavior.
* **Multi-threaded signal timing and vehicle spawning** for smooth real-time simulation.
* **Visual display** of traffic signals, timers, and vehicles using pygame graphics.

---

## How It Works

* Traffic signals cycle through green, yellow, and red states with predefined durations.
* Vehicles spawn randomly in different lanes and directions, moving at speeds depending on vehicle type.
* Emergency vehicles spawn at randomized intervals (\~1-1.5 minutes).
* Upon emergency vehicle detection, the system triggers a "heat situation" mode:

  * All signals turn blue for a brief pause.
  * Then, green signal is given exclusively to the emergency vehicle’s direction.
  * Other signals remain red until the emergency passes.
* The simulation visually updates vehicle positions and signal statuses continuously.

---

## Repository Structure

* `Simulation.py`: Main script containing all logic for traffic light control, vehicle spawning, movement, and emergency handling.
* `img/`: Contains images for vehicles, signals, and intersection background.
* `requirements.txt`: Python dependencies (pygame, etc.)

---

## Installation & Running

1. Clone the repository:

   ```bash
   git clone https://github.com/dhruvil-633/Intelligent-Traffic-Light-System.git
   cd Intelligent-Traffic-Light-System
   ```

2. Install dependencies:

   ```bash
   pip install pygame
   ```

3. Run the simulation:

   ```bash
   python Simulation.py
   ```

---

## Controls & Usage

* The simulation runs automatically with vehicle generation and signal cycling.
* To exit, close the pygame window or press the close button.
* The screen displays:

  * Traffic lights with timers at each intersection corner.
  * Vehicles moving along four directions.
  * Emergency vehicles appearing occasionally with prioritized green signals.

---

## Contributors

* **Manav Bachani**
* **Jiya Raval**

---

## Future Work

* Add adaptive signal timing based on real-time traffic density.
* Implement sensor input integration for real-world deployment.
* Expand simulation with pedestrian crossings and multi-intersection coordination.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
