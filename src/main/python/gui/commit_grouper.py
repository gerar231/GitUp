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

def __get_commit_hunks(commit, hunk_delimiter="\n"):
    message = commit.message
    if ":" in message:
        # remove the filename from the commit message.
        message = message[message.find(":") + 2:]
    return message.split(hunk_delimiter)

def group_commits_by_hunk(commits):
    result = {}
    hunk_to_commits = {}
    for commit in commits:
        hunks = __get_commit_hunks(commit)
        for hunk in hunks:
            if hunk not in hunk_to_commits:
                hunk_to_commits[hunk] = []
            hunk_to_commits[hunk].append(commit)
    for hunk in hunk_to_commits:
        commits = hunk_to_commits[hunk]
        commits_by_time = group_commits_by_time(commits)
        if hunk not in result:
            result[hunk] = []
        result[hunk] = commits_by_time
    return result
