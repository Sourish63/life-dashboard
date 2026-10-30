age=int(input("enter your age"))
cricket_hours=int(input("enter how many hours of cricket u play"))
gaming_hours=int(input("enter how many hours u spend on gaming"))
hobbies={"cricket":cricket_hours,"gaming":gaming_hours}
def time_hobbies():
  return(cricket_hours+gaming_hours)
total_hours=time_hobbies()
print("Age:",age)
for i in hobbies:
  print(i,hobbies[i])
def custom_joke():
  if age>=6:
      return(custom_joke=="I'm reading a book on gravity, and I just can't put it down")
  print("I'm reading a book on gravity, and I just can't put it down")
custom_joke()