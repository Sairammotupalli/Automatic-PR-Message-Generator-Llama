# Taking kilometers input from the user
miles = float(input("Enter value in kilometers: "))

# conversion factor
conv_fac = 1.60

# calculate miles
kilometers = miles * conv_fac 
print('%0.2f kilometers is equal to %0.2f miles' %(kilometers,miles))
