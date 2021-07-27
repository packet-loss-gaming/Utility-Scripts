#!/bin/bash

function cleanup() {
  echo -n "BACKUP_IN_PROGRESS=0" > /dev/udp/localhost/62895
}

trap cleanup EXIT
echo -n "BACKUP_IN_PROGRESS=1" > /dev/udp/localhost/62895
$@
