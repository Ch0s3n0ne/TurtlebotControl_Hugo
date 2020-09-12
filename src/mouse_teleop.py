#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import rospy
from turtlebot_control.srv import TurtleGoal

class GoalTeleop(object):
    """ Teleop class. Handles curses display and ROS communication. """

    def __init__(self, screen):
        """ Set up the display etc. """

        self._screen = screen
        curses.noecho()
        screen.keypad(1)
        screen.nodelay(1)
        curses.mousemask(1)

    def request_new_goal(self, x, y):
        """ Send the goal location and wait for a response.
        Returns True if the goal was reached, False otherwise.
        """
        rospy.wait_for_service('move_turtle_to_goal')
        try:
            set_turtle_goal = rospy.ServiceProxy('move_turtle_to_goal',
                                                 TurtleGoal)
            resp = set_turtle_goal(x, y)
        except rospy.ServiceException, e:
            resp = False
        return resp

    def run(self):
        """ Main loop.  Executes until the user presses q. """

        while True:
            self._screen.addstr(1, 1,
                                " Use the mouse to click a goal location.")
            self._screen.addstr(2, 1, "Press 'q' to quit.")

            event = self._screen.getch()
            if event == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                size_y, size_x = self._screen.getmaxyx()
                relative_x = mx / float(size_x)
                relative_y = (1.0 - my / float(size_y))
                try:
                    self._screen.addstr(my, mx, "X")
                except curses.error:
                    pass
                self._screen.refresh()
                self.request_new_goal(relative_x * 11.0, relative_y * 11.0)
                self._screen.clear()

            if event == ord("q"):
                break

            rospy.sleep(.05)

        curses.endwin()


def launch(screen):
    """ Created so that curses.wrapper can be used. """
    teleop = GoalTeleop(screen)
    teleop.run()


if __name__ == "__main__":
    curses.wrapper(launch)