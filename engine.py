#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import imutils
import numpy as np

import img_procession
import touchpad_manipulation as tmanip

def engine():
  frame_num = 0
  top, right, bottom, left = 10, 350, 225, 590
  aWeight = 0.5

  capture_video = cv2.VideoCapture( 0 )

  capture_video.set( 3, 320 )
  capture_video.set( 4, 240 )
  width = int( capture_video.get( cv2.CAP_PROP_FRAME_WIDTH ) + 0.5 )
  height = int( capture_video.get( cv2.CAP_PROP_FRAME_HEIGHT ) + 0.5 )

  four_cc = cv2.VideoWriter_fourcc( *'mp4v' )
  out = cv2.VideoWriter( 'output.mp4', four_cc, 20.0, ( 640, 480 ) )
  while( capture_video.isOpened() ):
    ret, frame = capture_video.read()

    if ret == True:
      frame = cv2.flip( frame, 1 )
      frame = imutils.resize( frame, width=640 )
      frame_cloned = frame.copy()
      roi = frame[top:bottom, right:left]
      gray = cv2.cvtColor( roi, cv2.COLOR_BGR2GRAY )
      gray = cv2.GaussianBlur( gray, ( 7, 7 ), 0 )

      if frame_num < 30:
        img_procession.run_avg( gray, aWeight )
      else:
        hand = img_procession.segment( gray )
        horizontal, vertical = img_procession.get_move_direction( gray )

        if horizontal == -1:
          tmanip.move_left()
        elif horizontal == 1:
          tmanip.move_right()

        if vertical == -1:
          tmanip.move_down()
        elif vertical == 1:
          tmanip.move_up()

        if hand is not None:
          ( threshold, segmented ) = hand
          cv2.drawContours( frame_cloned, [segmented + ( right, top )], -1, ( 0, 0, 255 ) )
          #cv2.imshow( "Thresholded", threshold )

      cv2.rectangle( frame_cloned, ( left, top ), ( right, bottom ), ( 0, 255, 0 ), 2 )
      frame_num += 1

      out.write( frame )

      #cv2.imshow( 'frame', frame )

      if ( cv2. waitKey( 1 ) & 0xFF ) == ord( 'q' ):
        break

    else:
      print( "Error happend. Is camera still working?" )
      break

  out.release()
  capture_video.release()
  cv2.destroyAllWindows()

if __name__=="__main__":
  engine()
