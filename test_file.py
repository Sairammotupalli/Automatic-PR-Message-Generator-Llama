# Taking kilometers input from the user
miles = float(input("Enter value in miles: "))

# conversion factor
conv_fac = 1.60

# calculate miles
kilometers = miles * conv_fac
print('%0.2f miles is equal to %0.2f kilometers' %(miles,kilometers))
