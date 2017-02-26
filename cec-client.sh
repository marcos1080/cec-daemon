#!/bin/bash

LOG="home/abe/.cec/cec-log.txt"
echo "" > $LOG

cec-client --log-file $LOG < /home/abe/.cec/cec_input
