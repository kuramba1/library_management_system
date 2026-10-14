numbers = [10, 20, 30, 40, 50]

print(numbers)
print(numbers[-1])
print(numbers[3:4])

numbers.append(10)
print(numbers)

numbers.extend([20, 30])
print(numbers)

numbers.remove(20)
print(numbers)

x = numbers.pop()
print("Element removed is", x)

print(50 in numbers)
print(len(numbers))
print(numbers.index(50))

numbers.insert(0, 100)
print(numbers)

# Duplicate the list
nubers3 = numbers.copy()
print(nubers3)
# set 
myset=(10,20,30,40)
print(type(myset))
print(myset)
myset1=(20,40,60,90)
# operation of sets
# 1.union
myset3=myset+myset1
print(myset3)
# intersection 
myset = {10, 20, 30, 40}
myset1 = {30, 40, 50, 60}

myset4 = myset1 & myset
print(myset4)
# remove item in a set 
myset1.remove(40)
print(myset1)

myset1 .discard(60)
print(myset1)

myset1.pop()
print(myset1)

myset1.pop()
print(myset1)

myset1.update({30, 50, 70, 100})  # Add multiple elements
print(myset1)


#dictionary
#a dictionary store data as key value pairs

person = {
    "name": "neza",
    "age": 30,
    "clases": "l5"
}

print(person)
#access values
       
print(person)
print(person["name"])#output neza

print(person.get("class"))#output l5

#add/updat element in dictionary
person["age"]=60 #update
print(person)


person["email"]="landrine@gmail.com"#add element
print(person)
#delet on eof items
person.pop("age")
print(person)

#del person name

del person["name"]
print(person)

