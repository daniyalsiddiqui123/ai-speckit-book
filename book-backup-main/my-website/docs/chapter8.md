---
title: "Chapter 8: Robot Locomotion"
---

# Chapter 8: Robot Locomotion

Robot locomotion refers to the various methods by which robots move through their environment. The choice of locomotion mechanism profoundly impacts a robot's mobility, stability, speed, and ability to traverse different terrains.

## Key Concepts

### Wheeled Locomotion
Wheeled robots are common due to their simplicity, speed, and energy efficiency on flat, structured surfaces.

*   **Types of Wheels:**
    *   **Standard Wheels:** Fixed orientation, used in differential drive or tricycle configurations.
    *   **Caster Wheels:** Passive, omnidirectional wheels for stability and turning.
    *   **Omnidirectional Wheels (Mecanum/Swedish Wheels):** Allow movement in any direction without changing wheel orientation, enabling complex maneuvers in confined spaces.
*   **Drive Systems:**
    *   **Differential Drive:** Two independently driven wheels with one or more passive caster wheels. Turning is achieved by varying the speed of the driven wheels.
    *   **Tricycle Drive:** One steerable driven wheel and two passive wheels.
    *   **Skid-Steer:** Similar to tracked vehicles, where turning is achieved by driving wheels on opposite sides at different speeds.
*   **Advantages:** High speed, energy efficiency, good stability on smooth surfaces.
*   **Disadvantages:** Limited mobility on uneven terrain, stairs, or obstacles.

### Legged Locomotion
Legged robots are designed to mimic biological systems, offering superior mobility over uneven, rough, or discontinuous terrains like stairs and debris.

*   **Types of Legged Robots:**
    *   **Bipedal Robots:** Two legs (e.g., humanoids). Challenging to balance, but highly versatile for human-centric environments.
    *   **Quadrupedal Robots:** Four legs (e.g., dog-like robots). Offer good stability and can carry heavier loads.
    *   **Hexapedal Robots:** Six legs (e.g., insect-like robots). Provide high stability, fault tolerance, and can traverse very complex terrain.
*   **Gait Generation:** The coordinated sequence of leg movements to achieve stable and efficient locomotion.
    *   **Static Gaits:** Maintain stability at all times by ensuring the center of gravity projection always falls within the support polygon (formed by the ground contact points of the legs). Slower, but highly stable.
    *   **Dynamic Gaits:** Allow for brief periods of instability, relying on momentum and rapid leg movements (e.g., running, trotting). Faster, but more complex control.
*   **Advantages:** High adaptability to various terrains, ability to step over obstacles.
*   **Disadvantages:** Complex control, higher energy consumption, slower speeds compared to wheeled robots on flat surfaces.

### Tracked Locomotion
Tracked robots use continuous tracks (like a tank) to move.

*   **Advantages:** Excellent traction on soft, loose, or uneven terrain (sand, mud, snow), good stability, ability to climb steep slopes and small obstacles.
*   **Disadvantages:** Lower speed, high turning resistance on firm ground (skid-steer), can damage delicate surfaces, higher maintenance.
*   **Applications:** Military, search and rescue, hazardous environment exploration.

### Aerial and Underwater Locomotion
These categories involve robots designed for movement in air and water, respectively.

*   **Aerial Locomotion (Drones/UAVs):** Utilize propellers or jets for flight.
    *   **Fixed-wing:** For long-endurance, high-speed flight.
    *   **Multi-rotor (quadcopters, hexacopters):** For vertical takeoff and landing (VTOL), hovering, and agile maneuvers.
*   **Underwater Locomotion (AUVs/ROVs):** Use propellers, thrusters, or bio-inspired methods.
    *   **AUVs (Autonomous Underwater Vehicles):** Pre-programmed or AI-driven for exploration, mapping.
    *   **ROVs (Remotely Operated Vehicles):** Tethred, human-controlled for inspection, intervention.

### Gait Generation and Stability
For legged robots, gait generation is the process of planning the sequence and timing of leg movements to achieve locomotion. Stability is a crucial concern, especially for dynamic gaits.

*   **Zero Moment Point (ZMP):** A key concept for bipedal and humanoid robot stability. It represents the point on the ground where the robot's generated ground reaction forces can effectively counteract the effects of gravity and inertia, keeping the robot balanced.
*   **Support Polygon:** The convex hull of all points where a robot's feet (or tracks) contact the ground. For static stability, the robot's center of mass projection must remain within this polygon.

## Learning Objectives

Upon completion of this chapter, you will be able to:

*   Differentiate between various types of robot locomotion, including wheeled, legged, and tracked systems, and their suitability for different environments.
*   Understand the principles behind wheeled robot movement and the advantages of omnidirectional wheels.
*   Explain the complexities of legged locomotion, including the classification of gaits (static vs. dynamic) and the balance challenges for bipedal robots.
*   Identify the unique characteristics and applications of aerial and underwater robots.
*   Grasp the concepts of gait generation and stability, including the Zero Moment Point (ZMP) for dynamic balance.

<h2>Further Reading</h2>

*   [Kelly, A. (2014). *Mobile Robotics: A Practical Introduction*. Cambridge University Press.](https://www.cambridge.org/core/books/mobile-robotics/3EDF4F5ED0B042F7B0B2E152F9424C58)
*   [Raibert, M. H. (1986). *Legged Robots That Balance*. MIT Press.](https://mitpress.mit.edu/books/legged-robots-balance)
