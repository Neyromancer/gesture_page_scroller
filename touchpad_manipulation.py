#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-

from pynput.mouse import Button, Controller
from AppKit import NSScreen

def scroll_page( x, y ):
  mouse = Controller()
  mouse.scroll( x, y )

def move_left():
  scroll_page( -5, 0 )

def move_right():
  scroll_page( 5, 0 )

def move_up():
  print( "mouse coord up {0}".format( -5 ) )
  scroll_page( 0, -5 )

def move_down():
  print( "mouse coord down {0}".format( 5 ) )
  scroll_page( 0, 5 )
