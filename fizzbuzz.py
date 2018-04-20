#!/usr/bin/python
# encoding: utf-8

def printer():
    for i in range(1, 101):
        if i%3==0 and i%5==0:
            print 'Fizz Buzz'
        elif i%3==0:
            print 'Fizz'
        elif i%5==0:
            print 'Buzz'
        else:
            print i



printer()