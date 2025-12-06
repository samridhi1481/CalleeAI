#!/usr/bin/env python3
import sys

# Tell Asterisk to play a builtin file
sys.stdout.write('STREAM FILE demo-echotest ""\n')
sys.stdout.flush()
