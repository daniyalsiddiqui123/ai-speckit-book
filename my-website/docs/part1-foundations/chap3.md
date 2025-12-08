---
title: "Chapter 3: Robot Dynamics"
---

# Chapter 3: Robot Dynamics

While kinematics describes the geometry of robot motion, dynamics investigates the relationship between the forces and torques acting on a robot and the resulting motion. Understanding robot dynamics is crucial for designing controllers, simulating robot behavior accurately, and performing force-controlled tasks.

## Key Concepts

### Newton-Euler Formulation
The Newton-Euler formulation is an iterative method for deriving the equations of motion for a robot manipulator. It applies Newton's second law and Euler's equation of motion (for rigid bodies) to each link of the robot, propagating forces and moments from the base to the end-effector (forward recursion) and then propagating velocities and accelerations back to the base (backward recursion).

*   **Forward Recursion (Kinematics):** Calculates velocities and accelerations of each link starting from the base.
*   **Backward Recursion (Dynamics):** Calculates forces and torques acting on each link, ultimately determining the joint torques required for a given motion.
*   **Advantages:** Computationally efficient for real-time control, especially for serial link manipulators.
*   **Disadvantages:** Can be less intuitive for conceptual understanding compared to Lagrangian methods.

### Lagrangian Dynamics
Lagrangian dynamics is an energy-based approach to derive the equations of motion. It formulates the dynamics in terms of the system's kinetic and potential energy, using the Euler-Lagrange equations. This method often leads to a more compact and elegant representation of the robot's dynamics.

*   **Lagrangian (L):** Defined as the difference between the kinetic energy (T) and potential energy (V) of the system (L = T - V).
*   **Euler-Lagrange Equation:** `d/dt (∂L/∂q̇_i) - ∂L/∂q_i = Q_i` (where `q_i` is a generalized coordinate, `q̇_i` is its time derivative, and `Q_i` is the generalized force/torque corresponding to `q_i`).
*   **Advantages:** Provides a systematic way to derive complex equations, often yielding more insightful results, and is suitable for systems with holonomic constraints.
*   **Disadvantages:** Can become cumbersome for very high-degree-of-freedom systems due to the complexity of energy calculations.

### Robot Manipulator Equations of Motion
Both Newton-Euler and Lagrangian formulations ultimately lead to a set of coupled, non-linear differential equations that describe the robot's motion. For a rigid robot manipulator with `n` degrees of freedom, the general form of the equation of motion is:

`M(q)q̈ + C(q, q̇)q̇ + G(q) = τ`

Where:
*   `M(q)`: The `n x n` mass matrix (or inertia matrix), which depends on the robot's configuration `q`.
*   `C(q, q̇)`: The `n x n` Coriolis and centrifugal forces matrix.
*   `G(q)`: The `n x 1` gravity vector.
*   `q`: The `n x 1` vector of joint positions (generalized coordinates).
*   `q̇`: The `n x 1` vector of joint velocities.
*   `q̈`: The `n x 1` vector of joint accelerations.
*   `τ`: The `n x 1` vector of joint torques (or forces for prismatic joints).

These equations are fundamental for dynamic analysis, simulation, and model-based control of robot manipulators.

### Dynamic Control
Dynamic control strategies utilize the robot's dynamic model to achieve precise and robust motion control, especially in tasks involving high speeds, significant payloads, or interaction with the environment.

*   **Computed Torque Control (or Inverse Dynamics Control):** A common model-based control technique that uses the dynamic model to calculate the joint torques required to achieve desired accelerations. It effectively linearizes and decouples the robot's dynamics.
*   **Adaptive Control:** Adjusts controller parameters online to compensate for uncertainties in the robot's dynamic model or changes in payload.
*   **Robust Control:** Designed to maintain performance despite model uncertainties and external disturbances.

## Learning Objectives

Upon completion of this chapter, you will be able to:

*   Apply the Newton-Euler formulation to derive the equations of motion for individual robot links.
*   Utilize Lagrangian dynamics to systematically derive the equations of motion for simple robot systems.
*   Understand and interpret the general form of the robot manipulator equations of motion, identifying the mass matrix, Coriolis/centrifugal terms, and gravity vector.
*   Explore basic concepts of dynamic control, such as computed torque control, and understand their role in achieving advanced robot performance.

## Further Reading

*   [Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2020). *Robot modeling and control*. John Wiley & Sons.](https://www.wiley.com/en-us/Robot+Modeling+and+Control%2C+2nd+Edition-p-9780470505191)
*   [Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G. (2009). *Robotics: Modelling, Planning and Control*. Springer Science & Business Media.](https://www.springer.com/gp/book/9781846286414)
