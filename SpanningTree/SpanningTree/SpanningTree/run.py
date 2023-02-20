#!/usr/bin/python

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
# Usage:
#     python run_spanning_tree.py <topology_file>
# For example, to run jellyfish_topo.py and log the results to jellyfish_topo.log, use the following command:
#     python run_spanning_tree.py jellyfish_topo
# Note that the topology file does NOT have the .py extension.
# Students should NOT modify this file.
#
# Copyright 2022 Vincent Hu
#           Based on prior work by Sean Donovan, Jared Scott, James Lohse, and Michael Brown

import sys
from Topology import *

PYTHON_VERSION = 3
PYTHON_RELEASE = 10

# Check python version
if sys.version_info < (PYTHON_VERSION, PYTHON_RELEASE):
    print("Warning:")
    print(f"    Please be sure you are using at least Python {PYTHON_VERSION}.{PYTHON_RELEASE}.x")
    exit()

if len(sys.argv) != 2:
    print("Syntax:")
    print("    python run_spanning_tree.py <topology_file>")
    exit()

topology_file = sys.argv[1]
# Check topology_file
if topology_file.endswith('.py'):
    print("Syntax:")
    print("Note that the topology file does NOT have the .py extension.")
    exit()

# Populate the topology
topo = Topology(topology_file)

# Run the topology
topo.run_spanning_tree()
# Close the logfile
topo.log_spanning_tree(f"{topology_file}.log")
