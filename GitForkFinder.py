
import requests
import csv
import click
import subprocess

@click.command()
@click.option('--repo', prompt='GitHub repo URL', help='URL of the GitHub repo to get forks from.')
@click.option('--token', prompt='GitHub Personal Access Token', help='Your GitHub Personal Access Token.')
@click.option('--output', default='forks.csv', help='Output CSV file name.')
def get_forks(repo, token, output):
    headers = {'Authorization': f'token {token}'}
    repo_name = repo.split("/")[-1]
    owner_name = repo.split("/")[-2]

    url = f"https://api.github.com/repos/{owner_name}/{repo_name}/forks"

    r = requests.get(url, headers=headers)
    forks = r.json()

    fork_data = []
    for fork in forks:
        fork_owner = fork['owner']['login']
        fork_url = fork['html_url']
        fork_git_url = fork['git_url']
        fork_created_at = fork['created_at']
        fork_updated_at = fork['updated_at']
        email = fork['owner']['email'] if 'email' in fork['owner'] else 'N/A'

        # Calculate the amount of change since fork creation and currently
        change_since_fork, current_change = calculate_amount_of_change(fork_git_url, repo, fork_created_at)

        # Get the number of commits posted to the repo by the fork owner
        commits_url = f"https://api.github.com/repos/{owner_name}/{repo_name}/commits?author={fork_owner}"
        r = requests.get(commits_url, headers=headers)
        num_commits = len(r.json())

        fork_data.append([fork_owner, email, fork_url, fork_updated_at, fork_updated_at, change_since_fork, num_commits])

    # Sort by amount_of_change and updated_at
    fork_data = sorted(fork_data, key=lambda x: (x[4], x[3]), reverse=True)

    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Fork Owner', 'Email', 'Fork URL', 'Updated At', 'Amount of Change', 'Number of Commits'])
        writer.writerows(fork_data)

def calculate_amount_of_change(fork_url, original_url, fork_creation_date):
    subprocess.call(["git", "clone", fork_url, "fork_repo"])
    subprocess.call(["git", "clone", original_url, "original_repo"])

    subprocess.call(["git", "-C", "fork_repo", "remote", "add", "upstream", original_url])
    subprocess.call(["git", "-C", "fork_repo", "fetch", "upstream"])

    # Calculate change since fork creation
    stats_since_fork = subprocess.check_output(["git", "-C", "fork_repo", "rev-list", "--left-right", "--count", f"{fork_creation_date}...master"])
    ahead_since_fork, behind_since_fork = map(int, stats_since_fork.decode().split())
    change_since_fork = ahead_since_fork + behind_since_fork

    # Calculate current change
    stats_current = subprocess.check_output(["git", "-C", "fork_repo", "rev-list", "--left-right", "--count", "master...upstream/master"])
    ahead_current, behind_current = map(int, stats_current.decode().split())
    current_change = ahead_current + behind_current

    subprocess.call(["rm", "-rf", "fork_repo"])
    subprocess.call(["rm", "-rf", "original_repo"])

    return change_since_fork, current_change

if __name__ == '__main__':
    get_forks()
