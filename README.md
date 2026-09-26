# LeetCode Streak Reminder

Checks daily whether you've made a LeetCode submission today, and sends a push
notification via ntfy if you haven't, at 9:30 PM and 10:30 PM IST.

## Known limitation: 60-day auto-disable

GitHub automatically disables a repo's scheduled Actions workflows if the repo
sees zero activity (commits, pushes, etc.) for 60 consecutive days. Since this
workflow runs (and therefore counts as activity) every single day, this should
never trigger in normal use — but if you ever stop actively using the repo for
an extended period and notice reminders have silently stopped, check:

Repo → Actions tab → if you see a banner saying the workflow is disabled,
click "Enable workflow" to reactivate it.
