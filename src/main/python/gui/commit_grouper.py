from datetime import date
import time
import git

# Returns a dictionary where keys are timestamps, and values are lists of
# commits that fall within those timestamps ordered from earliest time to
# latest time. Uses the commits in the input list to create this dictionary.
def group_commits_by_time(commits):
    result = {}
    for commit in commits:
        commit_date = date.fromtimestamp(commit.committed_date)
        if commit_date not in result:
            result[commit_date] = []
        result[commit_date].append(commit)
    # Sort all the commits from earliest time to latest time within each key
    for key in result:
        sorted_commits = sorted(result[key], key=lambda x : x.committed_date)
        result[key] = sorted_commits
    return result

