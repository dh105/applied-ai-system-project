# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Class 1: Pet: has attributes: owner_ids, pet_id, age, owner, task. Methods: getters that resturn the needs and the time they should be completed
another method that updates whether the task was met or not. 
Class 2: User: has attributes: onwner_id, pet_ids, schedule methods: 1- should return the free times of the user and match that with the pet. 
2- another method that creates a task for the pet based on the needs of the pet and the free time of the user.

Class 3: Task: has a pet_id, owner_id, type, allocated time, completed or not completed. It has method that keeps track of whether that task was fulfilled or not

Class 4: Scheduler: has a method that takes the user and pet info and creates a schedule based on the needs of the pet and the free time of the user.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

It added a priority attribut to the tasks to help the scheduling become more efficient. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
One constraint is the remaining time capacity (the slot capacity). In additon, it encforces no-overlap detection in detect_conflicts method. 
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The scheduler favors a simple greedy approach that schedules tasks in order of priority and earliest free time. This may leave time unusable if a longer task blocks a better combination of shorter tasks.

This is a tradeoff because it may not always produce the optimal schedule, but it is much simpler to implement and understand. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI using the brainstorming process and for debugging. It helped me create the initial UML design and it helped me with the algorithmic logic. 

The best prompts were the concise ones that involed a chat variable. For example, "#codebase What are the most important edge cases to test for a pet scheduler with sorting and recurring tasks?" 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I initially rejected the UML design it gave me because it was overly complex and had too many classes. I tried fixing it but it got more complicated. Therefore, I need to work on writing more concise prompts. 
I evaluated the UML diagram by looking at the Mermaid diagram and I noticed that it had too many classes. 

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

1- mark that a task is completed and check that the occurence is updated correctly. This is important because you do not want the user to have to manually add this task every time. 

2- test the explain function to make sure it returns the correct output. This is important because the user needs to understand the reasoning behind the schedule.

3- test the conflict detection to make sure it returns the correct warnings. This is important because the user needs to be aware of any conflicts in the schedule. It also ensures that the app doesn't crash when there are conflicts.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satified with the scheduling logic: that it considers priority and duration when scheduling the tasks. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would make the design consider some sort of idle time between tasksto allow for more flexibility in the schedule.

I would add other metrics to the tasks such as the energy levels of the pet and the user to make the scheduling more efficient. For example, if the pet is more active in the morning, the scheduler could prioritize scheduling tasks that require more energy in the morning. 

I would also make room to schedule at different times of the day, or specify the location of the event rather than choosing a limited contiguous timeframe from.  

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learnt that is important to evaluate the changes AI tools suggest before implementing them. Also, I go over the code after implementing the changes to make sure it is correct and efficient. In addition, I learnt how to use lambda functions to sort the tasks based on their scheduled time. 
# PawPal+ Agentic Workflow Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial Agentic Workflow is integrated in Pawpal design.
- What classes did you include, and what responsibilities did you assign to each?

The update includes agentic workflow elements, creating a scheduling agent that handles the scheduling logic and interacts with the user to gather necessary information for scheduling. The agent would be responsible for understanding user preferences, constraints, and generating a schedule accordingly.

Limitations it should tackle: 
    - handling priority considerations rather than the greedy approach of scheduling the shortest task first. 
    - ensuring that the generated schedule is feasible and efficient and considering the time constraints of the user and the pet's needs, e.g accouting for the break time and the energy levels of the pet and the user.
    - providing explanations for the generated schedule to help the user understand the reasoning behind it. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

It added a priority attribut to the tasks to help the scheduling become more efficient. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
One constraint is the remaining time capacity (the slot capacity). In additon, it encforces no-overlap detection in detect_conflicts method. 
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The scheduler favors a simple greedy approach that schedules tasks in order of priority and earliest free time. This may leave time unusable if a longer task blocks a better combination of shorter tasks.

This is a tradeoff because it may not always produce the optimal schedule, but it is much simpler to implement and understand. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI using the brainstorming process and for debugging. It helped me create the initial UML design and it helped me with the algorithmic logic. 

The best prompts were the concise ones that involed a chat variable. For example, "#codebase What are the most important edge cases to test for a pet scheduler with sorting and recurring tasks?" 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I initially rejected the UML design it gave me because it was overly complex and had too many classes. I tried fixing it but it got more complicated. Therefore, I need to work on writing more concise prompts. 
I evaluated the UML diagram by looking at the Mermaid diagram and I noticed that it had too many classes. 

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

1- mark that a task is completed and check that the occurence is updated correctly. This is important because you do not want the user to have to manually add this task every time. 

2- test the explain function to make sure it returns the correct output. This is important because the user needs to understand the reasoning behind the schedule.

3- test the conflict detection to make sure it returns the correct warnings. This is important because the user needs to be aware of any conflicts in the schedule. It also ensures that the app doesn't crash when there are conflicts.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satified with the scheduling logic: that it considers priority and duration when scheduling the tasks. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would make the design consider some sort of idle time between tasksto allow for more flexibility in the schedule.

I would add other metrics to the tasks such as the energy levels of the pet and the user to make the scheduling more efficient. For example, if the pet is more active in the morning, the scheduler could prioritize scheduling tasks that require more energy in the morning. 

I would also make room to schedule at different times of the day, or specify the location of the event rather than choosing a limited contiguous timeframe from.  

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learnt that is important to evaluate the changes AI tools suggest before implementing them. Also, I go over the code after implementing the changes to make sure it is correct and efficient. In addition, I learnt how to use lambda functions to sort the tasks based on their scheduled time. 
