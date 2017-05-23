#!/usr/bin/env python
# -*- coding=utf-8 -*-
#Using GPL v2
#Author: ihipop@gmail.com
##2010-10-27 22:07
"""
Usage:
Just A Template
"""
from __future__ import division
 
import sys,time
j = '#'
N=15
if __name__ == '__main__':
    for n in range(15):
        sys.stdout.write('\r')
        sys.stdout.write(' ' * (N+len(str(n))+1) +'|\r')
        sys.stdout.write(str(n)+'|')
        sys.stdout.flush()
        for i in range(N):
            sys.stdout.write('#')
            sys.stdout.flush()
            time.sleep(0.1)
print
