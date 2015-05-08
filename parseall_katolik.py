#!/bin/bash
for i in `ls katolik.pl/`
do
    echo "smth"
	/usr/bin/python parser_katolik.py katolik.pl/$i
done
