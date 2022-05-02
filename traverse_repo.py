#!/usr/bin/env python
from datetime import datetime, MINYEAR, MAXYEAR
from pydriller import Repository
from pydriller.metrics.process.contributors_count import ContributorsCount
from pydriller.metrics.process.commits_count import CommitsCount

REPO_URL = "git@github.com:numpy/numpy.git"
SINCE = datetime(2005, 1, 1)
TO = datetime(2022, 12, 31)
def get_data(
    repo_path,
    since=SINCE,
    to=TO,
):
    with open("test_history.csv", "w") as csvfile:
        csvfile.write("commit_hash,file,commit date,committer,old path,new path,change type,number of major contributors,number of minor contributors,number of commits to file\n")
        metric = ContributorsCount(repo_path, since=since, to=to)
        count = metric.count()
        minor = metric.count_minor()
        metric = CommitsCount(repo_path, since=since, to=to)
        num_commits = metric.count()
        for commit in Repository(repo_path, since=since, to=to).traverse_commits():
            print(commit.committer_date)
            for file in commit.modified_files:
                old_path = file.old_path if file.old_path is not None else ""
                new_path = file.new_path if file.new_path is not None else ""
                full_path = old_path if new_path is None else new_path
                if any(["test" in x for x in [old_path, new_path]]):
                    ct = 0 if full_path not in count else count[full_path]
                    mt = 0 if full_path not in minor else minor[full_path]
                    nc = 0 if full_path not in num_commits else num_commits[full_path]
                    csvfile.write(f"{commit.hash},{file.filename},{commit.committer_date},{commit.committer.name},{file.old_path},{file.new_path},{file.change_type.name},{ct},{mt},{nc}\n")

def main():
    get_data(REPO_URL)


if __name__ == "__main__":
    main()
