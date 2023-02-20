# Distance Vector project for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *


class DistanceVector(Node):

    __NEGATIVE_INIFITY__ = -99;
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """ Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        self.distanceVector = {self.name: 0};

    def send_initial_messages(self):
        """ This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight """

        self.__sendDVToUpstreams();

    def process_BF(self):
        """ This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. """

        isDVUpdated = False;

        for msg in self.messages:            
            isDVUpdated = self.__processMsg(msg) or isDVUpdated;
        
        # Empty queue
        self.messages = []
               
        if isDVUpdated:
            self.__sendDVToUpstreams();

    def log_distances(self):
        """ This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 """
               
        logstr = ",".join([ key + str(value) for key, value in self.distanceVector.items()]);
        add_entry(self.name, logstr);

    def __sendDVToUpstreams(self):
        for upstream in self.neighbor_names:
            self.send_msg((self.name, self.distanceVector), upstream);

    def __processMsg(self, msg):
        isDVUpdated = False;
        origin, originDV = msg;

        for nodeName in originDV:
            # ignore self node
            if nodeName == self.name:
                continue;

            # new node added to dv
            if nodeName not in self.distanceVector:
                cost = int(self.get_outgoing_neighbor_weight(origin));
                self.distanceVector[nodeName] = cost + originDV[nodeName];
                isDVUpdated = True;
            else:
                # negative cycle handler
                if originDV[nodeName] <= self.__NEGATIVE_INIFITY__ and self.distanceVector[nodeName] > self.__NEGATIVE_INIFITY__:
                    self.distanceVector[nodeName] = self.__NEGATIVE_INIFITY__;
                    isDVUpdated = True;
                    continue;
                # Bellman-Ford equation
                currentVal = self.distanceVector[nodeName];
                cost = int(self.get_outgoing_neighbor_weight(origin));
                self.distanceVector[nodeName] = max(min(cost + originDV[nodeName], currentVal), self.__NEGATIVE_INIFITY__);
                isDVUpdated = isDVUpdated or (self.distanceVector[nodeName] != currentVal);

        return isDVUpdated;

         

