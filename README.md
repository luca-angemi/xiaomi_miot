# Xiaomi Air Fryer

This is a custom component for home assistant to integrate the Xiaomi Air Fryer.

## Supported devices

| Name                        | Model                  | 
|  -------------------------  | ---------------------- | 
| Mi Smart Air Fryer          | careli.fryer.maf05a  | 
|                             | careli.fryer.maf10a  | 

## Features

### Mi Smart Air Fryer

* Buttons
 - Start cooking
 - Cancel cooking
 - Pause cooking
* Sensors
  - status
  - target_time
  - target_temperature
  - left_time
* Switch
  -  Start/Stop
* Select
  - target_time
  - target_temperature

## Install

Copy `xiaomi_air_fryer` folder to `custom_components` folder in your config folder.

Restart HA.

## Setup


1. With GUI. Configuration > Integration > Add Integration > Xiaomi Air Fryer
2. Enter your Xiaomi Account and Password
3. Select the Air Fryer device that you want to integrate.
