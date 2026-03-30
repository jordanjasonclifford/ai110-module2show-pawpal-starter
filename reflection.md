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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
