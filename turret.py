#!/usr/bin/python

import os
import sys
import time
import pygame
import usb.core

wavFile  = "warcry.wav"

cmdargs = []
currentTime = 0

class launchControl():
   def __init__(self):
      self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
      if self.dev is None:
         raise ValueError('Launcher not found.')
      if self.dev.is_kernel_driver_active(0) is True:
         self.dev.detach_kernel_driver(0)
      self.dev.set_configuration()

   def loopMovement(self, movement):
      
      while (True):
         if (time.time() - currentTime) > movement:
            self.turretStop()
            break

   def turretUp(self, movement):
      print("Turret Up.")
      self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

      self.loopMovement(movement)

   def turretDown(self, movement = 1000):
      print("Turret Down.")
      self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
      
      self.loopMovement(movement)

   def turretLeft(self, movement):
      print("Turret Left.")
      self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
      
      self.loopMovement(movement)

   def turretRight(self, movement):
      print("Turret Right.")
      self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
      
      self.loopMovement(movement)

   def turretStop(self):
      print("Turret Stop.")
      self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

   def turretFire(self):
      self.message1.set("FIRE!")

      if os.path.isfile(wavFile):
         if self.hasSound == True:
            pygame.init()
            sound = pygame.mixer.Sound("warcry.wav")
            sound.play()
            time.sleep(3)

      self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

   def setSound(self, soundOn):
      self.hasSound = soundOn

if __name__ == '__main__':

   if not os.geteuid() == 0:
       sys.exit("Script must be run as root.")
    
   # Get the total number of args passed to the turret.py
   total = len(sys.argv)

   # Get the arguments list 
   cmdargs = sys.argv
   
   if len(sys.argv) < 3:
      print("sudo ./turret.py <\"left\" | \"right\" | \"up\" | \"down\"> <duration of movement in milliseconds>")
      sys.exit()
   
   command = str.lower(cmdargs[1])
   
   if len(sys.argv) == 3:
      movement = int(cmdargs[2]) / 1000.0
   
   launchControl().setSound(True)
   
   currentTime = time.time();
   
   if command == "left":
       launchControl().turretLeft(movement)
 
   if command == "right":
       launchControl().turretRight(movement)
       
   if command == "up":
       launchControl().turretUp(movement)

   if command == "down":
       launchControl().turretDown(movement)
       
   if command == "fire":
       launchControl().turretFire()