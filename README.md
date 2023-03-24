# CINDERS
 <i>Cockpit Integrated Network Deployed Extinguisher Response System</i>
 
 Hello, and thanks for viewing CINDERS. I developed CINDERS in 2022 to support a testing environment where we needed to put out fires remotely.
 
 ![Screengrab](/screengrab.PNG)

 CINDERS is run via Python installed onto a RaspberryPi deployed on site. The RasPi GPIO pins control relays which trigger solenoids. These solenoids are connected to high-flow valves delivering CO2 from a tank to a test cell.
 By opening the solenoids, CO2 is injected into the test cell, displacing the air inside, until the fire is extinguished.
 
 The GUI is Tkinter, but there is also an option to control the system via command line if the user is forced to use SSH.
 
 Please note: Due to the fact CINDERS deals with concentrated CO2 and fire, <b>injury or death may occur if used improperly!</b> CINDERS is always employed with a safety officer on site and a fire station on call. CINDERS is not intended to be used with humans inside the test cell, or anywhere nearby.
 
 Anyone who uses CINDERS does so at their own risk, and this code is only presented for demonstration purposes. I deny any responsibility for damage to life or property that may occur due to use of this code or test cell design.
 
 Please read the overview slide deck to learn more. 
