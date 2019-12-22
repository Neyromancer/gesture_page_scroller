#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import imutils
import numpy as np

background = None
class LocalVariables:
  move_left = 640
  move_right = 0
  move_up = 0
  move_down = 480

class HCounter:
  count_sequence = 0
  prev_direction = 0

class VCounter:
  count_sequence = 0
  prev_direction = 0

def get_hdirection_without_fluctuation( move ):
  if HCounter.count_sequence == 0:
    HCounter.prev_direction = move
    HCounter.count_sequence = 1
  else:
    if HCounter.prev_direction == move:
      HCounter.count_sequence += 1

      if HCounter.count_sequence == 3:
        return move

    else:
      HCounter.count_sequence = 1
      HCounter.prev_direction = move

  return 0

def get_vdirection_without_fluctuation( move ):
  if VCounter.count_sequence == 0:
    VCounter.prev_direction = move
    VCounter.count_sequence = 1
  else:
    if VCounter.prev_direction == move:
      VCounter.count_sequence += 1

      if VCounter.count_sequence == 3:
        return move

    else:
      VCounter.count_sequence = 1
      VCounter.prev_direction = move

  return 0

# compute the running average between the current frame
# and the background model
def run_avg( image, aWeight ):
  global background

  if background is None:
    background = image.copy().astype( "float" )
    return

  cv2.accumulateWeighted( image, background, aWeight )

def segment( image, threshold=25 ):
  global background

  diff = cv2.absdiff( background.astype( "uint8" ), image )
  
  thresholded = cv2.threshold( diff, threshold, 255, cv2.THRESH_BINARY )[1]

  cnts, _ = cv2.findContours( thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

  if len( cnts ) == 0:
    return
  else:
    segmented = max( cnts, key = cv2.contourArea )
    return( thresholded, segmented )

def get_center( img_object ):
  if img_object is None:
    return (0, 0)

  ( threshold, segmented ) = img_object
  chull = cv2.convexHull( segmented )

  extreme_top = tuple( chull[chull[:, :, 1].argmin()][0] )
  extreme_bottom = tuple( chull[chull[:, :, 1].argmax()][0] )
  extreme_left = tuple( chull[chull[:, :, 0].argmin()][0] )
  extreme_right = tuple( chull[chull[:, :, 0].argmax()][0] )

  cX = int( ( extreme_left[0] + extreme_right[0] ) / 2 )
  cY = int( ( extreme_right[1] + extreme_bottom[0] ) / 2 )
  return ( cX, cY )

def get_move_direction( image ):
  hand = segment( image )

  cX, cY = get_center( hand )

  horizontal = 0
  vertical = 0

  if cX < LocalVariables.move_left - 5:
    print( "move_left" )
    LocalVariables.move_left = cX
    LocalVariables.move_right = 0
    horizontal = -1
  elif cX > LocalVariables.move_right + 5:
    print( "move_right" )
    LocalVariables.move_right = cX
    LocalVariables.move_left = cX
    horizontal = 1

  if cY < LocalVariables.move_down - 5:
    print( "move_down" )
    LocalVariables.move_down = cY
    LocalVariables.move_up = 0
    vertical = -1
  elif cY > LocalVariables.move_up + 5:
    print( "move_up" )
    LocalVariables.move_up = cY
    LocalVariables.move_down = cY
    vertical = 1

  horizontal = get_hdirection_without_fluctuation( horizontal )
  vertical = get_vdirection_without_fluctuation( vertical )

  return ( horizontal, vertical )
