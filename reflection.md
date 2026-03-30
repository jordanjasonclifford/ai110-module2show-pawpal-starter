# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    For the UML design, it would focus on four main classes. 
    This would include Owner, which would have the per owner's name and time available, and is the provider for the scheduler.
    The second class in Pet would include the name, breed, species, and the list of care tasks.
    The Task class be an activity, which can be the task name, time taken, and priority.
    Scheduler would the fourth and final class, in taking a owner's time and pet's tasks to then be sorted by priority and alloted time scheduled, in effort to return the plan for the owner to follow.



**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Nothing major was changed during implementation, just from the translation of the .js to the .py file; there was no reference to an owner actually owning a pet.
This was a silly mistake from the generation, and was fixed as the whole point of the system was for owners caring for their pets.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler mainly considers two things: the owner's available time for the day, and the priority of each task. 
It also takes into account whether a task has already been completed, so it won't re-schedule something that's done. 
I decided time and priority mattered most because those are the two things that actually limit what gets done in a day, you'd have a full list of tasks, but if you only have 30 minutes and a high-priority feeding to get to, that shapes everything else.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The biggest tradeoff is that the scheduler uses a greedy approach, adding tasks til time runs out. 
That means it could technically skip two short tasks that would have both fit, just because a longer high-priority task came first and used up most of the budget. 
A smarter algorithm could find the optimal combination, but that gets complicated fast. 
For a pet care app where the task list is small and the owner mostly just wants the important stuff handled first, greedy is good enough and a lot easier to follow.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

AI was used through every stage with some slight variation. Most of the brainstorming was done by me, with some AI use to help sharpen any issues. 
With the implementation, it helped me fill in logic as there's a lot of moving parts through it.
Most helpful prompts were specific like "how should conflict warnings be presented to a pet owner in app.py?"
Using specifics instead of like "add a conflict detection" made the suggestions more relevant to the AI

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One of the tests AI generated was for reset_recurring_tasks(), but it was giving a false positive so I cut it. I went back and used more specific prompts to figure out what was wrong with it, and that back and forth helped me rewrite it in a way that actually tested what the method was supposed to do.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The four main areas were tested with sorting, recurrence, conflict edetection, and edge cases. 
Sorting was with 'sort by time' always put the timed tasks first and didn't crash on an empty list.
For recurrence, daily tasks had to have a next-day copy and weekly tasks land throughout each week, with one-off tasks not spawning anything
Conflict detection had to catch overlaps and stay quiet with back-to-back tasks.
Edge cases cover pets without taks, and plan where everythings done with the owner not having availble time.

All behaviors were important as the app depends on it. Sorting makes the schedule, recurrence helps out in terms of not reinputting schedules, conflict detection warns the user if any overlaps, and edge cases in place for no errors shown to user.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

The core logic made me confident, with all tests passing and covering anything I could think of. 
The UI layer isn't tested as compared to main, so with more time I would test invalid time formats, two pets with same name, and check the reset button.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I love the logic of how the schedule prioritizes different tasks, this feature would be a great idea to add within say a 'to-do' app personal project to follow

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Session states could be reset with refereshes, with some sort of logging system of a 'database' would be best. This could even be done in a txt file due to the low stakes nature of the project but of course would be needed to be scaled up if expanded upon greatly.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI is great when you have the understanding of what you're building at a given time. 
Knowing what prompts to make at a given time and being very specific can net you better results. A vague prompt will NOT get you far when using AI as a companion.