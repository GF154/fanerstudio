#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration pytest
"""

import sys
import io

# Disable stdout/stderr redirection for tests
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

