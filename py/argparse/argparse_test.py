#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 参考 https://www.jianshu.com/p/fef2d215b91d
import argparse
parser = argparse.ArgumentParser(description="your script description")

parser.add_argument('test', help='file or directory names list for speed benchmark') #必选参数 根据出现传入的顺序去定值
parser.add_argument('em', help='list of e-mail addresses to send warnings')


parser.add_argument('-e', help='可选参数') #需要指定值
parser.add_argument('--verbosity', '-v', action='store_true', help='more verbose logs', default=False) #不需要指定值
args = parser.parse_args()

print(args)

if args.verbosity:
    print("打开 verbosity")
