def minPlanesReq(fuelUnits):
    n = len(fuelUnits)
    switches = 0
    balFuel = fuelUnits[0]	# balance fuel for initial take-off

    for i in range(1, n):	# iterate throug list to reach destination
        if balFuel == 0:	# return -1 in the case if there are still points left to reach destination but fuel isn't enough
            return -1

        balFuel -= 1		# with each iteration reducing the fuel content by 1

        if balFuel == 0:
            switches += 1
            balFuel = fuelUnits[i]	# updating the balance fuel to next in line location

    return switches			# returns the number of planes required


# Example usage:
fuelUnits = [2, 1, 0, 0, 1]
op = minPlanesReq(fuelUnits) # function that return the number of planes required to reach deatination
print(op)  # Output: 3
