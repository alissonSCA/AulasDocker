#!/bin/bash

# Verifica se o SSH está rodando
if pgrep -x "sshd" > /dev/null; then
    exit 0
else
    exit 1
fi
