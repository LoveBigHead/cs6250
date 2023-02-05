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
# Copyright 2022 Vincent Hu
#           Based on prior work by Sean Donovan, Jared Scott, James Lohse, and Michael Brown

from Message import *
from StpSwitch import *


class Switch(StpSwitch):
    """
    This class defines a Switch (node/bridge) that can send and receive messages
    to converge on a final, loop-free spanning tree. This class
    is a child class of the StpSwitch class. To remain within the spirit of
    the project, the only inherited members or functions a student is permitted
    to use are:

    switchID: int
        the ID number of this switch object)
    links: list
        the list of switch IDs connected to this switch object)
    send_message(msg: Message)
        Sends a Message object to another switch)

    Students should use the send_message function to implement the algorithm.
    Do NOT use the self.topology.send_message function. A non-distributed (centralized)
    algorithm will not receive credit. Do NOT use global variables.

    Student code should NOT access the following members, otherwise they may violate
    the spirit of the project:

    topolink: Topology
        a link to the greater Topology structure used for message passing
    self.topology: Topology
        a link to the greater Topology structure used for message passing
    """

    def __init__(self, idNum: int, topolink: object, neighbors: list):
        """
        Invokes the super class constructor (StpSwitch), which makes the following
        members available to this object:

        idNum: int
            the ID number of this switch object
        neighbors: list
            the list of switch IDs connected to this switch object
        """
        super(Switch, self).__init__(idNum, topolink, neighbors)

        self.rootID = idNum;
        self.distanceToRoot = 0;
        self.activeLinks = [];
        self.switchThrough = self.rootID;


    def process_message(self, message: Message):
        """
        Processes the messages from other switches. Updates its own data (members),
        if necessary, and sends messages to its neighbors, as needed.

        message: Message
            the Message received from other Switches
        """
        # print("Before processing");
        # self.__printState();
        # self.__printMsg(message);

        if message.root > self.rootID:
            return
        elif message.root == self.rootID:
            self.__equalRootHandler(message);
        else:
            self.__defaultHandler(message);

        # print("After processing");
        # self.__printState();
        # print("===================================");

    def generate_logstring(self):
        """
        Logs this Switch's list of Active Links in a SORTED order

        returns a String of format:
            SwitchID - ActiveLink1, SwitchID - ActiveLink2, etc.
        """
        activeLinksStrs = [];
        self.activeLinks.sort();

        for activeLink in self.activeLinks:
            activeLinksStrs.append("{0} - {1}".format(self.switchID, activeLink));
             
        return ", ".join(activeLinksStrs);

    def __equalRootHandler(self, message: Message):
        newDistanceToRoot = message.distance + 1;

        if newDistanceToRoot <  self.distanceToRoot:
            self.distanceToRoot = newDistanceToRoot;
            self.__updateSwitchThrough(message.origin);
            self.__sendMsgToNeighbors();
        elif newDistanceToRoot == self.distanceToRoot:
            if message.origin < self.switchThrough:
                self.__updateSwitchThrough(message.origin);
                self.__sendMsgToNeighbors();
        else:
            if message.pathThrough:
                self.activeLinks.append(message.origin);
            elif message.origin in self.activeLinks:
                self.activeLinks.remove(message.origin);

    def __defaultHandler(self, message: Message):
        self.rootID = message.root;
        self.distanceToRoot = message.distance + 1;
        self.__updateSwitchThrough(message.origin);

        self.__sendMsgToNeighbors();

    def __sendMsgToNeighbors(self):
        for neighbor in self.links:
            msg = Message(self.rootID, self.distanceToRoot, self.switchID, neighbor, neighbor == self.switchThrough);
            self.send_message(msg);

    def __updateSwitchThrough(self, newSwitchThrough):
        self.activeLinks.clear();
        self.switchThrough = newSwitchThrough;
        self.activeLinks.append(self.switchThrough);

    # def __printMsg(self, msg: Message):
    #     print("origin: {0}, destination: {1}, root: {2}, distance: {3}, pathThrough: {4}".format(msg.origin, msg.destination, msg.root, msg.distance, msg.pathThrough));

    # def __printState(self):
    #     print("id: {0}, root: {1}, distance: {2}, switchthrough: {3}".format(self.switchID, self.rootID, self.distanceToRoot, self.switchThrough));
    #     print(self.activeLinks);
    #     print("*****************");

