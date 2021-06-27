#!/bin/bash

# ./roms.sh file(s) path 192.168.192.58 pi raspberry
files=$1
path=$2
ip=$3
user=$4
pwd=$5

if [ "$1" = "-h" ]
then
  echo "help"
  exit 1
elif [ -v $1 ]
then
  echo "no files"
  exit 0
elif [ -v $2]
then
  echo "no path"
  exit 0
fi

if [ -v $3 ]
then
  ip="192.168.192.58"
fi
if [ -v $4 ]
then
  user="pi"
fi
if [ -v $5 ]
then
  pwd="raspberry"
fi

sshpass -p "$pwd" scp $file $user@$ip:/home/$user/Ras/$path/
sshpass -p "$pwd" ssh $user@$ip ''
