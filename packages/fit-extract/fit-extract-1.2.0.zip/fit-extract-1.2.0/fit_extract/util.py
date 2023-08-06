#!/usr/bin/env python
import glob
import os


def correctPath(path):
    """Fixes path name"""
    return os.path.normpath(path) + '/'


def pathToName(filepath):
    """Returns an extensionless name from a file path
    >>> pathFoo = 'C://Users//User//Folder//Subfolder//foo_C07.fit'
    >>> path = 'C://Users//User//Folder//Subfolder//'
    >>> pathToName(pathFoo)
    'foo_C07'
    """
    fileWithExtension = os.path.split(filepath)[1]
    return os.path.splitext(fileWithExtension)[0]


def nameToChannel(name):
    """Returns the channel from the name of a file
    >>> name = 'foo_C07'
    >>> nameToChannel(name)
    '7'
    >>> name = 'foo_C12'
    >>> nameToChannel(name)
    '12'
    """
    channelString = name.split('_')[-1]
    if channelString[1] == '0':
        return channelString[-1]
    return channelString[1:]


def getFitFilePaths(path=''):
    """Returns a list of file paths with .fit extension"""
    return glob.glob(path + '*.fit')


def ParamFromSearchParam(searchParam):
    """
    >>> ParamFromSearchParam('R1 =')
    'R1'
    """
    return searchParam[:-2]


def SearchParamFromParam(param):
    """
    >>> SearchParamFromParam('R1')
    'R1 ='
    """
    return param + ' ='
