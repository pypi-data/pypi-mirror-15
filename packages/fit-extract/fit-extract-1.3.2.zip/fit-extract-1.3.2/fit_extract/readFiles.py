#!/usr/bin/env python
from .readLines import *


def createFile(filepath, name, paramToValue, numberOfCycles=1):
    """Creates a dictionary storing file information"""
    File = {'filepath': filepath,
            'name': name,
            'paramToValue': paramToValue,
            'numberOfCycles': numberOfCycles}
    return File


def getValue(File, param, cycle=-1):
    return File['paramToValue'][param][cycle]


def setValue(File, param, value, cycle=-1):
    File['paramToValue'][param][cycle] = value


def getCycleRange(File):
    return range(File['numberOfCycles'])


def getFilePath(File):
    return File['filepath']


def getName(File):
    return File['name']


######## Barrier ########


def swapValues(File, paramsToSwap, cycle=-1):
    """Swaps the values of two parameters (p1, p2)"""
    p1 = paramsToSwap[0]
    p2 = paramsToSwap[1]
    v1 = getValue(File, p1, cycle)
    v2 = getValue(File, p2, cycle)
    setValue(File, p1, v2, cycle)
    setValue(File, p2, v1, cycle)


def groupParamsBySize(File, paramsToGroupBySize, has_cycles):
    """Groups parameterss by size"""
    p1 = paramsToGroupBySize[0]
    p2 = paramsToGroupBySize[1]
    if has_cycles:
        for cycle in getCycleRange(File):
            v1 = getValue(File, p1, cycle)
            v2 = getValue(File, p2, cycle)
            if v1 > v2:
                swapValues(File, (p1, p2), cycle)
    else:
        v1 = getValue(File, p1)
        v2 = getValue(File, p2)
        if v1 > v2:
            swapValues(File, (p1, p2))


def extract(params, filepath):
    """Extract values and units of params for a file"""
    searchParams = [SearchParamFromParam(p) for p in params]
    paramToValue = {p: [] for p in params}
    paramToUnit = {}
    with open(filepath, 'r') as f:
        for line in f:
            for sp in searchParams:
                if sp in line:
                    p = ParamFromSearchParam(sp)
                    paramToValue[p].append(lineToValue(line))
                    paramToUnit[p] = getUnit(line)
    return paramToValue, paramToUnit


def extractFolder(params, path, paramsToGroupBySize, has_cycles):
    """Extracts values and units from files in a folder"""
    filepaths = getFitFilePaths(path)
    Files = []
    assert filepaths  # For skip / exit messages
    for filepath in filepaths:
        paramToValue, paramToUnit = extract(params, filepath)
        name = pathToName(filepath)
        File = createFile(filepath, name, paramToValue,
                          len(paramToValue[params[0]]))
        if paramsToGroupBySize:
            groupParamsBySize(File, paramsToGroupBySize, has_cycles)
        Files.append(File)
    return paramToUnit, Files
