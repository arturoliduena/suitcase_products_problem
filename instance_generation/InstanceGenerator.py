'''
AMMM P2 Instance Generator v2.0
Instance Generator class.
Copyright 2020 Luis Velasco.

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

import os, random
from AMMMGlobals import AMMMException


class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        caseWidth = self.config.caseWidth
        caseHeight = self.config.caseHeight
        caseCapacity = self.config.caseCapacity
        numItems = self.config.numItems

        minPricePerItem = self.config.minPricePerItem
        maxPricePerItem = self.config.maxPricePerItem

        minWeightPerItem = self.config.minWeightPerItem
        maxWeightPerItem = self.config.maxWeightPerItem

        minSidePerItem = self.config.minSidePerItem
        maxSidePerItem = self.config.maxSidePerItem

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            # caseWidth = random.uniform(minCaseWidth, maxCaseWidth)
            # caseHeight = random.uniform(minCaseHeight, maxCaseHeight)
            # caseCapacity = random.uniform(minCaseCapacity, maxCaseCapacity)

            itemPrice = [0] * numItems
            for t in range(numItems):
                itemPrice[t] = random.uniform(minPricePerItem, maxPricePerItem)

            itemWeight = [0] * numItems
            for t in range(numItems):
                itemWeight[t] = random.uniform(minWeightPerItem, maxWeightPerItem)

            itemSide = [0] * numItems
            for t in range(numItems):
                itemSide[t] = random.uniform(minSidePerItem, maxSidePerItem)

            itemPrice = map(int, itemPrice)
            itemWeight = map(int, itemWeight)
            itemSide = map(int, itemSide)

            """
            An instance needs to contain:
            caseWidth: int - width of the suitcase
            caseHeight: int - height of the suitcase
            caseCapacity: int - weight capacity of the suitcase
            n: int - number of items to pick from
            price: int[] - list of length n containing item prices
            weight: int[] - list of length n containing item weights
            side: int[] - list of length n containing item side lengths
            """

            fInstance.write('caseWidth=%d;\n' % caseWidth)
            fInstance.write('caseHeight=%d;\n' % caseHeight)
            fInstance.write('caseCapacity=%d;\n' % caseCapacity)

            fInstance.write('n=%d;\n' % numItems)

            # translate vector of floats into vector of strings and concatenate that strings separating them by a single space character
            fInstance.write('price=[%s];\n' % (' '.join(map(str, itemPrice))))
            fInstance.write('weight=[%s];\n' % (' '.join(map(str, itemWeight))))
            fInstance.write('side=[%s];\n' % (' '.join(map(str, itemSide))))

            fInstance.close()
