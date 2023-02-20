"""
/*
 * Copyright © 2022 Georgia Institute of Technology (Georgia Tech). All Rights Reserved.
 * Template code for CS 6250 Computer Networks
 * Instructors: Maria Konte
 * Head TAs: Johann Lau and Ken Westdorp
 *
 * Georgia Tech asserts copyright ownership of this template and all derivative
 * works, including solutions to the projects assigned in this course. Students
 * and other users of this template code are advised not to share it with others
 * or to make it available on publicly viewable websites including repositories
 * such as GitHub and GitLab. This copyright statement should not be removed
 * or edited. Removing it will be considered an academic integrity issue.
 *
 * We do grant permission to share solutions privately with non-students such
 * as potential employers as long as this header remains in full. However,
 * sharing with other current or future students or using a medium to share
 * where the code is widely available on the internet is prohibited and
 * subject to being investigated as a GT honor code violation.
 * Please respect the intellectual ownership of the course materials
 * (including exam keys, project requirements, etc.) and do not distribute them
 * to anyone not enrolled in the class. Use of any previous semester course
 * materials, such as tests, quizzes, homework, projects, videos, and any other
 * coursework, is prohibited in this course.
 */
"""

# Spanning Tree Protocol project for GA Tech OMSCS CS-6250: Computer Networks
#
# Defines a Message: message sent from one node to another using Spanning Tree Protocol.
# Students should not modify this file.
#
# Copyright 2022 Vincent Hu
#           Based on prior work by Sean Donovan, Jared Scott, James Lohse, and Michael Brown


class Message(object):

    def __init__(self, claimedRoot: int, distanceToRoot: int, originID: int, destinationID: int, pathThrough: bool):
        """
        root: int
            the ID of the switch thought to be the root by the origin switch
        distance: int
            the distance of the origin to the root
        origin: int
            the ID of the origin switch (sender)
        destination: int
            the ID of the destination switch (receiver)
        pathThrough: bool
            indicating the path to the claimed root from the origin passes through the destination
        """
        self.root = claimedRoot
        self.distance = distanceToRoot
        self.origin = originID
        self.destination = destinationID
        self.pathThrough = pathThrough

    def verify_message(self):
        """
        Member function that returns True if the message is properly formed, and False otherwise
        """
        valid = True

        if self.pathThrough != True and self.pathThrough != False:
            valid = False
        if isinstance(self.root, int) is False or isinstance(self.distance, int) is False or \
                isinstance(self.origin, int) is False or isinstance(self.destination, int) is False:
            valid = False

        return valid
