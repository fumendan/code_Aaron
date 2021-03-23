#!/usr/bin/env python3
# coding=utf-8

import sys
import os

BASEPATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASEPATH)

from man import manage

if __name__ == '__main__':
    manage.man()