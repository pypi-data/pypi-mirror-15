*********************
Shock Tube Calculator
*********************

Description
===========

This module calculates a Riemann problem for Euler equation:

.. math::

  \frac{\partial}{\partial t}\left(\begin{array}{c}\rho\\ \rho u\\\rho E \end{array}\right) + 
  \frac{\partial}{\partial x}\left(\begin{array}{c}\rho u\\ \rho u^2\\\rho uE + pu \end{array}\right) = 0

where :math:`\rho`, :math:`u`, :math:`E` is a fluid density, velocity and total energy, respectively.
The  total energy can be expressed as sum of specific internal (:math:`e = \frac{p}{\gamma -1}`) and kinetic energy: :math:`E = e+\frac{1}{2}u^2`, where :math:`p` and :math:`\gamma` denote the fluid pressure and specific heat ratio.

Standard test case
------------------

A shock tube consists of a long tube filled with the same gas in two different physical states. The tube is divided into two parts, separated by a diaphragm. The initial state is defined by the values for density, pressure and velocity.

.. image:: images/shock_tube_t0.png
   :width: 200 px
   :alt: alternate text
   :align: center

When the membrane bursts, discontinuity between the two initial states breaks into leftward and rightward moving waves, separated by a contact surface.

.. image:: images/shock_tube_t_n.png
   :width: 200 px
   :alt: alternate text
   :align: center

- Region 5 is the low pressure gas which is not disturbed by the shock wave.
- Regions 3 and 4 (divided by the contact surface) contain the gas immediately behind the shock traveling at a constant speed.
- The contact surface across which the density and the temperature are discontinuous lies within this zone.
- The zone between the head and the tail of the expansion fan is noted as Region 2. In this zone, the flow properties gradually change since the expansion process is isentropic.
- Region 1 denotes the undisturbed high pressure gas.


The density :math:`\rho` and pressure :math:`p` on the left are unity, while the density on the right side of the contact and pressure are set to 0.125 and 0.1, respectively. The ratio of specific heats is 1.4



Usage
=====

.. code:: python

  from shocktubecalc import sod

  # left_state and right_state set p, rho and u
  # geometry sets left boundary on 0., right boundary on 1
  # and initial position of the shock xi on 0.5
  # t is the time evolution for which positions and states in tube should be calculated
  # gamma denotes specific heat
  # npts is number of points to be calculated for rarefaction wave
  # Note that gamma and npts are default parameters (1.4 and 500) in solve function.

  positions, regions, values = sod.solve(left_state=(1, 1, 0), right_state=(0.1, 0.125, 0.),
                                         geometry=(0., 1., 0.5), t=0.2, gamma=1.4, npts=500)



Return value of a :code:`solve` function
----------------------------------------

The :code:`positions` is a dictionary of region names and their positions in the pipe after t=0.2 seconds.

Printing positions for each and every region: 

.. code:: python

  print('Positions:')
  for desc, vals in positions.items():
      print('{0:10} : {1}'.format(desc, vals))


The :code:`regions` is a dictionary of constant pressure, density and velocity for all regions except for the rarefaction wave. 

.. code:: python

  print('States:')
  for desc, vals in regions.items():
      print('{0:10} : {1}'.format(desc, vals))


The :code:`values` is a dictionary of :math:`p`, :math:`\rho`, :math:`u` :math:`x` arrays. If one would want to plot said values as a function of  :math:`x`: 

.. code:: python

  import matplotlib.pyplot as pl
  plt.figure(1)
  plt.plot(values['x'], values['p'], linewidth=1.5, color='b')
  plt.ylabel('pressure')
  plt.xlabel('x')
  plt.axis([0, 1, 0, 1.1])

  plt.figure(2)
  plt.plot(values['x'], values['rho'], linewidth=1.5, color='r')
  plt.ylabel('density')
  plt.xlabel('x')
  plt.axis([0, 1, 0, 1.1])

  plt.figure(3)
  plt.plot(values['x'], values['u'], linewidth=1.5, color='g')
  plt.ylabel('velocity')
  plt.xlabel('x')

  plt.show()

Calculating other values
------------------------

- Internal energy :math:`e = p/(\gamma-1)`
- Temperature :math:`T = p/\rho`
- Speed of sound :math:`c = \sqrt{\gamma p/\rho}` 
- Mach number :math:`M = u/c`:

.. code:: python

  E = values['p']/(gamma -1)
  T = values['p']/values['rho']
  c = np.sqrt(gamma *values['p']/values['rho'])
  M = values['p']/c




