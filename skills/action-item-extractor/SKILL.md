---
name: action-item-extractor
description: Extract concrete action items from meetings, emails, and documents - identifies what needs to be done, by whom, and when
---

# Action Item Extractor

Turn discussions into executable tasks.

## Overview

Every meeting, email, and document contains work that needs to happen. "We should update the docs." "Can someone check the metrics?" "Let's review this next week."

Most of these tasks get forgotten. This skill extracts them, assigns ownership, and makes them trackable.

You're a task parser, not a meeting summarizer. Find concrete actions that need to happen, identify who should do them, flag the deadlines. Turn vague discussions into clear next steps.

## When to Use

Use after any communication with actionable work:
- Meeting notes or transcripts
- Email threads with requests
- Project discussions or planning docs
- Slack conversations with action items
- Bug reports or feature requests
- Customer feedback requiring follow-up
- Brainstorming sessions with next steps

Don't use for:
- Pure status updates (no actions needed)
- Completed work (historical only)
- Informational content without tasks
- Decisions without execution steps

## The Process

**First, scan for action language:**
Look for task indicators:
- "Should", "need to", "must", "have to"
- "Can someone", "who will", "I'll", "we'll"
- Question form: "Could we...", "Can you...", "Who can..."
- Directive: "Please", "make sure to", "remember to"
- Future work: "next step", "follow up", "before launch"

**Then, extract the components:**
For each action item, identify:
1. **What** - The specific task or deliverable
2. **Who** - Owner or assignee (if specified)
3. **When** - Deadline or timeframe (if specified)
4. **Context** - Why it matters or what it blocks
5. **Status** - Implied urgency or priority

**Categorize by clarity:**
- **Clear:** Has owner, task, and deadline
- **Partial:** Missing deadline or owner
- **Vague:** Needs clarification before actionable
- **Implied:** Action suggested but not explicit

**Prioritize by urgency:**
- **URGENT:** Blocking work, explicit deadline imminent
- **HIGH:** Important, clear timeline within days
- **MEDIUM:** Should be done, timeline within weeks
- **LOW:** Nice to have, no specific timeline

**Finally, structure the output:**
- List all action items clearly
- Group by owner or priority
- Flag missing components (no owner, no deadline)
- Highlight blockers and dependencies

## Action Item Indicators

**Explicit Tasks:**
- "Please send the report"
- "I'll update the docs by Friday"
- "Sarah will review the code"
- "We need to fix the bug before launch"

**Implicit Tasks:**
- "The docs are outdated" → Someone should update them
- "Has anyone checked the logs?" → Someone needs to check logs
- "We're missing test coverage" → We need to add tests

**Questions as Tasks:**
- "Can someone verify the numbers?" → Verify numbers
- "Who owns the API work?" → Assign owner to API work
- "Should we update the design?" → Decide on design update

**Conditional Tasks:**
- "If approved, deploy to staging" → Deploy (if approved)
- "Once legal reviews, send to client" → Send to client (after legal)

## Output Format

Keep it actionable. Show what needs to be done, by whom, and when.

```
✅ ACTION ITEMS
━━━━━━━━━━━━━━━━━━━━

Source: [Meeting/Email/Doc Title]
Date: [When these were identified]
Total Items: 8 (3 urgent, 2 high, 2 medium, 1 low)

━━━━━━━━━━━━━━━━━━━━
🔥 URGENT
━━━━━━━━━━━━━━━━━━━━

#1 - Fix production bug
Owner: Sarah (Engineering)
Deadline: TODAY by EOD
Context: Blocking customer signups
Status: ⚠️ Critical blocker
Dependencies: None

#2 - Send contract to legal
Owner: Mike (Sales)
Deadline: Today 3pm
Context: Client waiting for signature
Status: ⚠️ Time-sensitive
Dependencies: Final pricing approved

#3 - Deploy hotfix to production
Owner: DevOps team
Deadline: Within 2 hours
Context: Follows bug fix (#1)
Status: ⚠️ Blocked by #1
Dependencies: Bug fix completed

━━━━━━━━━━━━━━━━━━━━
⚡ HIGH PRIORITY
━━━━━━━━━━━━━━━━━━━━

#4 - Review API documentation
Owner: Alex (Product)
Deadline: Friday, Feb 2
Context: Launch prep
Status: On track
Dependencies: None

#5 - Update onboarding flow
Owner: Design team
Deadline: End of week
Context: User feedback implementation
Status: ⚠️ No specific owner assigned
Dependencies: User research findings

━━━━━━━━━━━━━━━━━━━━
📋 MEDIUM PRIORITY
━━━━━━━━━━━━━━━━━━━━

#6 - Add metrics to dashboard
Owner: Jordan (Analytics)
Deadline: Next sprint
Context: Better visibility for stakeholders
Status: In planning

#7 - Schedule customer interviews
Owner: Unassigned
Deadline: This month
Context: Feature validation
Status: ⚠️ Needs owner

━━━━━━━━━━━━━━━━━━━━
💡 LOW PRIORITY
━━━━━━━━━━━━━━━━━━━━

#8 - Explore new logging solution
Owner: Engineering
Deadline: None specified
Context: Current system slow but working
Status: ⚠️ No deadline

━━━━━━━━━━━━━━━━━━━━
⚠️  ISSUES & GAPS
━━━━━━━━━━━━━━━━━━━━

• Item #5: Design team mentioned but no specific owner
• Item #7: No owner assigned - needs someone to take this
• Item #8: No deadline - add to backlog or set timeline?
• Missing: Who will communicate launch timeline to customers?

━━━━━━━━━━━━━━━━━━━━
📊 SUMMARY BY OWNER
━━━━━━━━━━━━━━━━━━━━

Sarah (Engineering): 1 urgent
Mike (Sales): 1 urgent
DevOps team: 1 urgent (blocked)
Alex (Product): 1 high
Design team: 1 high (no specific owner)
Jordan (Analytics): 1 medium
Engineering: 1 low
Unassigned: 1 medium

━━━━━━━━━━━━━━━━━━━━
⏰ TIMELINE VIEW
━━━━━━━━━━━━━━━━━━━━

Today:
  #1 - Fix production bug (Sarah) [URGENT]
  #2 - Send contract (Mike) [URGENT]
  #3 - Deploy hotfix (DevOps) [URGENT, BLOCKED]

This Week:
  #4 - Review API docs (Alex) [HIGH]
  #5 - Update onboarding (Design) [HIGH]

Next Week+:
  #6 - Add metrics (Jordan) [MEDIUM]
  #7 - Schedule interviews (Unassigned) [MEDIUM]

No Deadline:
  #8 - Explore logging (Engineering) [LOW]
```

## Extraction Examples

**From Meeting Notes:**
```
Input: "We should update the documentation before launch. Sarah mentioned
she'll fix the bug today. Has anyone looked at the metrics dashboard?"

Output:
#1 - HIGH: Update documentation (no owner, deadline: before launch)
#2 - URGENT: Fix bug (Sarah, deadline: today)
#3 - MEDIUM: Review metrics dashboard (no owner, implied task from question)
```

**From Email:**
```
Input: "Can someone send me the latest designs? Also, we need to schedule
a follow-up meeting with the client. I'll review the contract this afternoon."

Output:
#1 - HIGH: Send latest designs (no owner, requestor waiting)
#2 - MEDIUM: Schedule client meeting (no owner, no deadline)
#3 - HIGH: Review contract (sender, deadline: this afternoon)
```

**From Slack Thread:**
```
Input: "The staging environment is down. @DevOps can you look into this?
Meanwhile, I'll check if anyone reported this bug in production."

Output:
#1 - URGENT: Fix staging environment (@DevOps, immediate)
#2 - HIGH: Check production bug reports (sender, immediate)
```

**From Project Discussion:**
```
Input: "We discussed adding authentication. If we go with OAuth, someone
needs to research providers. The team agreed to prototype next sprint."

Output:
#1 - MEDIUM: Research OAuth providers (no owner, conditional on decision)
#2 - HIGH: Build auth prototype (team, deadline: next sprint)
```

## Common Patterns

**Implicit Ownership:**
"I think we should add tests" → Speaker likely volunteers
"Can you look into X?" → Addressee is owner
"Let's do Y" → Needs explicit owner assignment

**Vague Tasks:**
"We should improve performance" → What specifically? Set metrics
"Update the docs" → Which docs? What sections?
Break vague tasks into specific sub-tasks or flag for clarification.

**Cascading Tasks:**
"Fix bug, then deploy, then notify customers"
→ Three tasks with dependencies
Track the chain explicitly.

**Conditional Tasks:**
"If approved, start development"
→ Mark as CONDITIONAL and note the trigger

**Recurring Tasks:**
"Send weekly reports"
→ Mark as RECURRING and specify frequency

## Priority Scoring

**URGENT (Do today):**
- Explicit "today", "ASAP", "immediately"
- Blocking other work or people
- Production issues or customer impact
- Hard deadline within 24 hours

**HIGH (Do this week):**
- Explicit deadline within days
- Important for upcoming milestone
- Requested by stakeholder or customer
- Impacts team velocity if delayed

**MEDIUM (Do this month):**
- Deadline within weeks
- Improves process or quality
- Follow-up from decision
- Not blocking current work

**LOW (Backlog):**
- No deadline specified
- Nice to have improvements
- Exploratory or research tasks
- Can be deferred indefinitely

## Do's and Don'ts

**DO:**
- Extract every actionable task, even small ones
- Identify owner even if implicit ("I'll" = speaker)
- Flag missing owners or deadlines
- Prioritize by urgency and impact
- Break vague tasks into specifics when obvious
- Note dependencies between tasks
- Mark questions as implied tasks

**DON'T:**
- Skip implicit tasks (questions often hide actions)
- Miss conditional tasks ("if X, do Y")
- Ignore tasks because they're small
- Confuse decisions with actions (decision ≠ task)
- Miss cascading tasks (do X, then Y, then Z)
- Forget recurring tasks (weekly, monthly)
- Treat discussions as tasks (talking about ≠ doing)

## Watch Out For

**Hidden tasks in discussions:**
"We talked about improving performance" → Not a task yet
"We should improve performance" → Implied task

**Ownership ambiguity:**
"The team will handle it" → WHO on the team?
"Someone should check" → WHO is someone?
→ Flag as UNASSIGNED

**Deadline vagueness:**
"Soon", "shortly", "when we can" → No real deadline
→ Flag as NO DEADLINE

**Blocked tasks:**
"Once legal approves, we'll deploy" → Blocked by legal
"After the meeting, send the notes" → Blocked by meeting
→ Track the blocker explicitly

**Competing priorities:**
Same person assigned multiple urgent tasks
→ Flag OVERALLOCATION

## Integration Workflows

**After meetings:**
1. Run action item extractor on notes
2. Assign unowned items to specific people
3. Set deadlines for vague timelines
4. Export to project management tool
5. Send summary to participants

**Email triage:**
1. Extract action items from inbox
2. Prioritize by urgency
3. Delegate or schedule
4. Archive email once tasks are tracked
5. Follow up on unresponded items

**Project planning:**
1. Extract all tasks from project doc
2. Break down large tasks into sub-tasks
3. Assign owners and deadlines
4. Map dependencies
5. Track in sprint or kanban board

**Daily standup:**
1. Extract blockers as urgent tasks
2. Extract "will do today" as tasks
3. Track who's doing what
4. Follow up on yesterday's tasks

## Key Principles

- **Every action has three parts:** What, Who, When (flag if missing)
- **Urgency is relative:** Compare to other tasks and deadlines
- **Questions hide tasks:** "Can someone X?" = "Do X"
- **Implicit ownership counts:** "I'll" = task for speaker
- **Dependencies block execution:** Track them explicitly
- **Vague tasks need clarification:** Break down or flag
- **Small tasks matter:** Don't skip them, they add up

## Your Checklist

For every action item you extract:
- [ ] What needs to be done (specific, actionable)
- [ ] Who should do it (person/team, flag if missing)
- [ ] When it's due (date/timeframe, flag if missing)
- [ ] Why it matters (context or what it blocks)
- [ ] Priority level (urgent/high/medium/low)
- [ ] Dependencies (blocked by what/whom)
- [ ] Status flags (unassigned, no deadline, vague, blocked)

## Works Well With

Combine with these other skills:
- **/commitment-tracker** - Track promises vs. action items
- Project management tools - Export tasks directly
- Meeting notes - Extract tasks automatically
- Email filters - Auto-extract from tagged emails

## Remember

Action items are the bridge between discussion and execution. If someone says "should", "need to", or asks "can someone", that's work waiting to happen.

Your job is to find every piece of work, assign it to someone, set a deadline, and flag what's missing. Don't let tasks hide in conversations. Make them concrete, trackable, and actionable.

The difference between productive teams and chaos is often just writing down who's doing what by when.
