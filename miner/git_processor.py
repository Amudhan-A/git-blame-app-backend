import git
import re
from shared.types import CommitInfo, GitContext


def mine_git_history(repo_path: str, filepath: str, function_name: str):

    repo = git.Repo(repo_path)

    commits = []

    for commit in repo.iter_commits(paths=filepath):

        message = commit.message
        issues = re.findall(r"#(\d+)", message)

        diff_text = ""

        if commit.parents:
            parent = commit.parents[0]

            diffs = commit.diff(parent, paths=filepath, create_patch=True)

            for diff in diffs:
                diff_text += diff.diff.decode("utf-8", errors="ignore")

        commit_info = CommitInfo(
            sha=commit.hexsha,
            message=message,
            author=str(commit.author),
            date=str(commit.committed_datetime),
            diff_snippet=diff_text,
            linked_issues=issues
        )

        commits.append(commit_info)

    return GitContext(
        repo=repo_path,
        filepath=filepath,
        function_name=function_name,
        commits=commits,
        prs=[]
    )