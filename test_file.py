# Taking kilometers input from the user
miles = float(input("Enter value in miles: "))

# conversion factor
conv_fac = 1/0.621371

# calculate miles
kilo = miles * conv_fac
print('%0.2f miles is equal to %0.2f kilometers' %(miles,kilo))
