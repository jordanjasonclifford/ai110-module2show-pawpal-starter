classDiagram
    class Owner {
        +String name
        +int timeAvailable
        +Pet pet
        +getAvailableTime()
    }

    class Pet {
        +String name
        +String breed
        +String species
        +List~Task~ tasks
        +addTask(task)
        +removeTask(task)
        +getTasks()
        +getPendingTasks()
        +getCompletedTasks()
    }

    class Task {
        +String taskName
        +int duration
        +String priority
        +bool completed
        +String scheduledTime
        +String recurrence
        +Date dueDate
        +getDetails()
        +markComplete()
    }

    class Scheduler {
        +generatePlan(owner, pet)
        +sortByTime(tasks)
        +detectConflicts(plan)
        +conflictWarnings(plan, petName)
        +detectCrossPetConflicts(petPlans)
        +markTaskComplete(pet, task)
        +resetRecurringTasks(pet)
        +filterByPet(pets, petName)
        -_sortTasks(tasks)
        -_sortByPriority(tasks)
        -_fitWithinTime(tasks, timeAvailable)
        -_timeToMinutes(timeStr)
    }

    Owner "1" --> "0..1" Pet : owns
    Pet "1" *-- "many" Task : has
    Scheduler --> Owner : reads time from
    Scheduler --> Pet : reads and modifies tasks from
    Scheduler --> Task : modifies