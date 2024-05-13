'''
AMMM P2 Instance Generator v2.0
Config attributes validator.
Copyright 2020 Luis Velasco

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from AMMMGlobals import AMMMException


class ValidateConfig(object):
    # Validate config attributes read from a DAT file.

    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        paramList = ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                     'caseWidth', 'caseHeight',
                     'caseCapacity', 'numItems',
                     'minPricePerItem', 'maxPricePerItem',
                     'minWeightPerItem', 'maxWeightPerItem',
                     'minSidePerItem', 'maxSidePerItem'
                     ]

        for paramName in paramList:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter(%s) has not been not specified in Configuration' % str(paramName))

        instancesDirectory = data.instancesDirectory
        if len(instancesDirectory) == 0: raise AMMMException('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if len(fileNamePrefix) == 0: raise AMMMException('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if len(fileNameExtension) == 0: raise AMMMException('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if not isinstance(numInstances, int) or (numInstances <= 0):
            raise AMMMException('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        # Case width
        caseWidth = data.caseWidth
        if not isinstance(caseWidth, int) or (caseWidth <= 0):
            raise AMMMException('caseWidth(%s) has to be a positive integer value.' % str(caseWidth))

        # Case height
        caseHeight = data.caseHeight
        if not isinstance(caseHeight, int) or (caseHeight <= 0):
            raise AMMMException('caseHeight(%s) has to be a positive integer value.' % str(caseHeight))

        # Case capacity
        caseCapacity = data.caseCapacity
        if not isinstance(caseCapacity, int) or (caseCapacity <= 0):
            raise AMMMException('caseCapacity(%s) has to be a positive integer value.' % str(caseCapacity))

        # Num items
        numItems = data.numItems
        if not isinstance(numItems, int) or (numItems <= 0):
            raise AMMMException('minCaseCapacity(%s) has to be a positive integer value.' % str(numItems))

        # Price per item
        minPricePerItem = data.minPricePerItem
        if not isinstance(minPricePerItem, int) or (minPricePerItem <= 0):
            raise AMMMException('minPricePerItem(%s) has to be a positive integer value.' % str(minPricePerItem))

        maxPricePerItem = data.maxPricePerItem
        if not isinstance(maxPricePerItem, int) or (maxPricePerItem <= 0):
            raise AMMMException('maxPricePerItem(%s) has to be a positive integer value.' % str(maxPricePerItem))

        if maxPricePerItem < minPricePerItem:
            raise AMMMException('maxPricePerItem(%s) has to be >= minPricePerItem(%s).' % (
            str(maxPricePerItem), str(minPricePerItem)))

        # Weight per item
        minWeightPerItem = data.minWeightPerItem
        if not isinstance(minWeightPerItem, int) or (minWeightPerItem <= 0):
            raise AMMMException('minWeightPerItem(%s) has to be a positive integer value.' % str(minWeightPerItem))

        maxWeightPerItem = data.maxWeightPerItem
        if not isinstance(maxWeightPerItem, int) or (maxWeightPerItem <= 0):
            raise AMMMException('maxWeightPerItem(%s) has to be a positive integer value.' % str(maxWeightPerItem))

        if maxWeightPerItem < minWeightPerItem:
            raise AMMMException('maxWeightPerItem(%s) has to be >= minWeightPerItem(%s).' % (
            str(maxWeightPerItem), str(minWeightPerItem)))

        # Side per item
        minSidePerItem = data.minSidePerItem
        if not isinstance(minSidePerItem, int) or (minSidePerItem <= 0):
            raise AMMMException('minSidePerItem(%s) has to be a positive integer value.' % str(minSidePerItem))

        maxSidePerItem = data.maxSidePerItem
        if not isinstance(maxSidePerItem, int) or (maxSidePerItem <= 0):
            raise AMMMException('maxSidePerItem(%s) has to be a positive integer value.' % str(maxSidePerItem))

        if maxSidePerItem < minSidePerItem:
            raise AMMMException('maxSidePerItem(%s) has to be >= minSidePerItem(%s).' % (
            str(maxSidePerItem), str(minSidePerItem)))
