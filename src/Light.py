#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:18:01 2019

@author: Atte Torri
"""

import numpy as np
import math
from abc import abstractmethod

from Ray import *
from Shape import *
from Bounding_Box import *

class Light:
    
    # Compute how much light gets to a given point
    @abstractmethod
    def shadow(self, r_point, ray, obj, bbox):
        pass
    
    def all_shadows(r_point, ray, obj, bbox, lights):
        result_brightness = 0.0
        for light in lights:
            result_brightness += light.shadow(r_point, ray, obj, bbox)
        return result_brightness

class Ambient_Light(Light):
    
    def __init__(self, brightness):
        self.brightness = brightness
        
    def shadow(self, r_point, ray, obj, bbox):
        return self.brightness

class Point_Light(Light):
    
    def __init__(self, point, brightness):
        self.point = point
        self.brightness = brightness
    
    def shadow(self, r_point, ray, obj, bbox):
        norm_vect = obj.calculate_norm_vect(r_point, ray)
        vect_to_light = self.point-r_point
        # Calculate distance to light source
        dist = np.linalg.norm(vect_to_light)
        # Calculate shadow ray towards light source
        shadow_ray = Ray(r_point, vect_to_light, None)
        # Compute closest object in shadow ray trajectory
        t, closest = bbox.find_closest(shadow_ray)
        #print('t', t)
        # Verify if object is in the way
        if(dist < t or t==-1):
            # Angle between shadow ray and object normal vector
            # TODO : Find out why np.pi- required
            angle = np.pi-math.acos((norm_vect@shadow_ray.vect)/(np.linalg.norm(norm_vect)*np.linalg.norm(shadow_ray.vect)))
            if(abs(angle) < np.pi/2):
                # How much light is dimmed by the angle
                angle_factor = (np.pi/2-abs(angle))/np.pi*2
                # How much light is dimmed by the distance
                dist_factor = 1/(dist**2)
                # If light has been set to be equally bright at every distance
                if(self.brightness == -1):
                    return angle_factor
                return dist_factor*angle_factor*self.brightness
        # Return no light
        return 0
    
class Plane_Light(Light):
    
    def __init__(self, point, norm_vect, brightness=-1):
        self.point = point
        self.norm_vect = norm_vect
        self.brightness = brightness
        
class Sphere_Light(Light):
    pass