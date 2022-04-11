#!/usr/bin/env python
"""
GDC Task - Python
Applicant - Kiran Kumari
"""
import sys


def Usage():
    """
    Prints the documentation on how to use commands.
    """
    print("Usage :-")
    print("$ ./task.py add 2 hello world    # Add a new item with priority 2 and text \"hello world\" to the list")
    print("$ ./task.py ls                   # Show incomplete priority list items sorted by priority in ascending order")
    print("$ ./task.py del INDEX            # Delete the incomplete item with the given index")
    print("$ ./task.py done INDEX           # Mark the incomplete item with the given index as complete")
    print("$ ./task.py help                 # Show usage")
    print("$ ./task.py report               # Statistics")


def getPrioritynum_and_name(line):
    """
    Gets the priority number and name of a task from the lines of task.txt
    """
    var = list(line.split(" "))
    num = int(var[0])
    name = " ".join(var[1:])
    return num , name


def arrange_tasklist():
    """
    Arranges the tasks in required priority order. Called every time a new task is added.
    """
    task_list = []
    with open('task.txt','r') as file:
        lines = file.read().splitlines()    
    with open('task.txt','w') as file:
        for x in lines:

            number , name = getPrioritynum_and_name(x)
            task_list.append((number,name))
   
        task_list.sort(key = lambda x:x[0])
        for x in task_list:
            file.write(f"{x[0]} {x[1]}\n")



def gettaskName_byindex_or_Priority(num , find_by):
    """
    Gets the name of the task by index number or Priority number depending on the input string.
    Returns None if no task available.
    """
    with open("task.txt","r") as file:
        lines = file.read().splitlines()
        for index,x in enumerate(lines):

            Pri_number , name = getPrioritynum_and_name(x)
            if find_by == "index":
                if num == (index+1):
                    return name
            elif find_by == "pri":
                if num == Pri_number:
                    return name

    return None



def getPriority_byTaskName(tname):
    """
    Returns the priority number of a task if task is found else returns -1.
    """
    with open("task.txt","r") as file:
        lines = file.read().splitlines()
        for x in lines:

            Pri_number , name = getPrioritynum_and_name(x)
            if name == tname:
                return Pri_number

    return -1

def deletetask_byindex(num):
    """
    Deletes a task from task.txt by the index order in the file.
    """

    with open("task.txt","r") as file:
        lines = file.read().splitlines()

    with open("task.txt",'w') as file:

        task_deleted = False
        for index,x in enumerate(lines):
            pr_number , name = getPrioritynum_and_name(x)
            
            if num == (index+1):
                print("Deleted:" ,name)
                task_deleted = True                
            else:
                file.write(f"{pr_number} {name}\n")

    return task_deleted

def clear_list():
    """
    Extra Function : To clear both the task list and completed list. Resets basically.
    """
    file = open('task.txt','r')
    if file:
        new = open('task.txt','w')
        new.close()

    file.close()

    file = open('Completed.txt','r')
    if file:
        new = open('Completed.txt' , 'w')
        new.close()

    file.close()

def list_task():
    """
    Corresponding function to listing the incomplete task and displays them on the screen.
    """
    
    try:
        with open('task.txt','r') as file:
            lines = file.read().splitlines()
            if len(lines) == 0:
                print("There are no pending tasks!")
                return

            for index,x in enumerate(lines):
                Pri_number , name = getPrioritynum_and_name(x)
                print(f"{index+1}. {name} [{Pri_number}]")
    except:
        print("There are no pending tasks!")


def delete_task(num):
    """
    Corresponding function to deleting a task from the list when user enters its index.
    Calls deletetask_by_index function and returns appropriate messages if task is not found.
    """                 
    deleted = deletetask_byindex(num)
    if deleted == False:
        print(f"Error: task with index #{num} does not exist. Nothing deleted.")
    else:
        print(f"Deleted task #{num}")        

def mark_donetask(num):
    """
    Corresponding function to mark a task as done. Checks whether the task is already completed.
    Avoids duplicate addition to Completed list. If the task is present in the incomplete list,it deletes it from task and appends to completed list.
    """

    with open("Completed.txt",'r') as file:
        lines_1 = file.read().splitlines()


    with open("Completed.txt",'a') as file:

        task_name = gettaskName_byindex_or_Priority(num,"index")
        
        if ((task_name != None) and (task_name not in lines_1)) :
            
            file.write(f"{task_name}\n")

    deleted = deletetask_byindex(num)
    if deleted == True:
        print("Marked item as done.")
    else:
        print(f"Error: no incomplete item with index #{num} exists.")


def report():
    """
    Prints the number of complete and incomplete tasks and also their names with their priority order.
    """

    with open('task.txt','r') as file1:
        lines = file1.read().splitlines()
        print("Pending :", len(lines))

        for index,x in enumerate(lines):
            Pri_num , name = getPrioritynum_and_name(x)
            print(f"{index+1}. {name} [{Pri_num}]")
    
    print()

    with open('Completed.txt','r') as file2:
        lines = file2.read().splitlines()
        print("Completed :", len(lines))

        for index , x in enumerate(lines):
            print(f"{index+1}. {x}")
        


def add_task(num , tname):
    """
    Function to add a task name and its priority number to the task list. It checks if the task is already
    present with a different priority number in that case, it does not add. It also checks whether that task 
    is already in completed list. If yes, it removes the task from the completed list and adds to incomplete 
    tasks list. It also arranges the task list according to priority by making another function call.
    """

    with open('task.txt','a+') as file:

        task_priority = getPriority_byTaskName(tname)   # getting -1 means the task does not exist
        if task_priority == -1:
            file.write(f"{num} {tname}\n")
            print(f"Added task: \"{tname}\" with priority {num} ")

        elif task_priority != int(num):
            print(f"task already exists with priority {task_priority}")
  
        else:
            print(f"Added task: \"{tname}\" with priority {num} ")

        with open('Completed.txt','a+') as second:
            lines = second.read().splitlines()

        with open('Completed.txt','w') as second:

            for x in lines:
                if x != tname:
                    second.write(f"{x}\n")

    arrange_tasklist()





if __name__ == "__main__":

    length_input = len(sys.argv)

    if length_input == 1 or (length_input == 2 and sys.argv[1] == 'help'):
        Usage()

    elif length_input > 1:

        comm = sys.argv[1]
        if  comm == 'add' :

            if length_input > 2:

                priority = sys.argv[2]

                if len(" ".join(sys.argv[3:])) != 0:     # takes both quotes and non-quotes from terminal
                    task_name = " ".join(sys.argv[3:])
                    add_task(priority , task_name)

            else:
                print("Error: Missing tasks string. Nothing added!") 

        elif  comm == 'ls' and length_input==2 :
            list_task()

        elif comm == 'clearall' and length_input==2 :
            clear_list()
        
        elif comm == 'del' :

            if length_input == 3:
                delete_task(int(sys.argv[2]))
            else:
                print("Error: Missing NUMBER for deleting tasks.")
        
        elif  comm == 'done' :

            if length_input == 3 :
                mark_donetask(int(sys.argv[2]))
            else:
                print("Error: Missing NUMBER for marking tasks as done.")

        elif  comm == 'report' :
            report()
        
