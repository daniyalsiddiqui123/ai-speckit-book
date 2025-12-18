---
title: "Chapter 7: Robot Actuators and Grippers"
---

# Chapter 7: Robot Actuators and Grippers

Actuators are the "muscles" of a robot, responsible for converting energy into motion, allowing the robot to move its joints and interact with the physical world. Grippers (or end-effectors) are specialized actuators designed to grasp, hold, and manipulate objects. Together, they enable robots to perform physical tasks.

## Key Concepts

### Electric Motors
Electric motors are the most common type of actuator in robotics due to their precision, efficiency, and ease of control.

*   **DC Motors:** Simple, inexpensive, and provide high torque at low speeds. Often used with gearboxes for increased torque.
    *   **Brushed DC Motors:** Require brushes for commutation, leading to wear.
    *   **Brushless DC (BLDC) Motors:** More efficient, longer lifespan, higher power density, and better control due to electronic commutation.
*   **Stepper Motors:** Move in discrete steps, allowing for precise position control without feedback (open-loop control) in many applications.
    *   **Advantages:** Simple control for positioning.
    *   **Disadvantages:** Can lose steps under high load, lower efficiency.
*   **Servo Motors:** Consist of a DC or BLDC motor, a gearbox, and a position feedback sensor (encoder). Designed for precise position, velocity, and torque control (closed-loop control).
    *   **Advantages:** High precision, high torque, good dynamic response.
    *   **Applications:** Robot joints, CNC machines.

### Hydraulic and Pneumatic Actuators
These actuators use pressurized fluids (hydraulic, typically oil) or gases (pneumatic, typically air) to generate powerful linear or rotary motion.

*   **Hydraulic Actuators:**
    *   **Advantages:** Very high force/power density, precise control (when combined with servo valves).
    *   **Disadvantages:** Messy (oil leaks), requires hydraulic power unit, less efficient than electric motors for many applications.
    *   **Applications:** Heavy industrial robots, construction machinery.
*   **Pneumatic Actuators:**
    *   **Advantages:** Clean, fast response, simple control for on/off actions, relatively inexpensive.
    *   **Disadvantages:** Lower force/power density than hydraulic, harder to achieve precise position/force control.
    *   **Applications:** Simple pick-and-place, assembly, emergency stop systems.

### Gear Trains and Transmissions
Gear trains are mechanical systems that transmit power and motion between rotating components, primarily used to change the speed and torque of a motor's output to meet the robot's requirements.

*   **Function:** Reduce speed and increase torque (or vice-versa).
*   **Types:** Spur, helical, bevel, worm gears, planetary gearboxes, harmonic drives.
*   **Harmonic Drives:** Known for high gear ratios, low backlash, and compact size, making them popular in precision robotic manipulators.
*   **Backlash:** The lost motion due to clearance between mating gear teeth, which can reduce precision.

### Types of Grippers
Grippers are end-effectors designed to grasp and manipulate objects. Their design is highly task-dependent.

*   **Two-Finger Grippers (Parallel or Angular):** Simple, common for industrial pick-and-place.
    *   **Parallel:** Fingers move parallel to each other.
    *   **Angular:** Fingers pivot open and close.
*   **Multi-Finger Grippers (Articulated):** More complex, often resembling human hands, capable of grasping irregularly shaped objects and performing dexterous manipulation.
*   **Vacuum Grippers (Suction Cups):** Use negative pressure to pick up objects with smooth, flat surfaces.
    *   **Advantages:** Non-marring, good for delicate or uneven surfaces, fast.
    *   **Disadvantages:** Requires smooth surfaces, not suitable for porous materials.
*   **Adhesive Grippers:** Use sticky materials or electrostatic forces to adhere to objects.
*   **Underactuated Grippers:** Have fewer actuators than degrees of freedom in their fingers, allowing them to conform to object shapes passively.

### Force and Torque Sensing in Grippers
Integrating force and torque sensors into grippers or wrists allows robots to delicately handle objects, apply controlled forces, and detect contact. This is crucial for tasks requiring fine manipulation and interaction with sensitive environments or humans.

*   **Applications:** Assembly of delicate parts, polishing, human-robot collaboration.
*   **Benefits:** Prevents damage to objects, provides haptic feedback, enables adaptive grasping.

## Learning Objectives

Upon completion of this chapter, you will be able to:

*   Identify and describe different types of electric motors (DC, stepper, servo) and their typical applications in robotics.
*   Understand the working principles and trade-offs of hydraulic and pneumatic actuators.
*   Explain the role of gear trains and transmissions in robotic systems, including specialized drives like harmonic drives.
*   Categorize and differentiate between various types of grippers, including multi-finger, vacuum, and underactuated designs.
*   Grasp the importance of force and torque sensing in grippers for delicate manipulation and interactive tasks.

<h2>Further Reading</h2>

*   [Niku, S. B. (2010). *Introduction to Robotics: Analysis, Control, Applications*. Wiley.](https://www.wiley.com/en-us/Introduction+to+Robotics%3A+Analysis%2C+Control%2C+Applications-p-9780470604467)
*   [Murray, R. M., Li, Z., & Sastry, S. S. (1994). *A mathematical introduction to robotic manipulation*. CRC press.](https://www.taylorfrancis.com/books/mathematical-introduction-robotic-manipulation-richard-murray-zexiang-li-s-sastry/9780849379819)
