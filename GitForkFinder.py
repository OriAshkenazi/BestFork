
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
        fork_updated_at = fork['updated_at']
        email = fork['owner']['email'] if 'email' in fork['owner'] else 'N/A'

        # Calculate the amount of change
        amount_of_change = calculate_amount_of_change(fork_git_url, repo)

        fork_data.append([fork_owner, email, fork_url, fork_updated_at, amount_of_change])

    # Sort by amount_of_change and updated_at
    fork_data = sorted(fork_data, key=lambda x: (x[4], x[3]), reverse=True)

    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Fork Owner', 'Email', 'Fork URL', 'Updated At', 'Amount of Change'])
        writer.writerows(fork_data)

def calculate_amount_of_change(fork_url, original_url):
    subprocess.call(["git", "clone", fork_url, "fork_repo"])
    subprocess.call(["git", "clone", original_url, "original_repo"])

    subprocess.call(["git", "-C", "fork_repo", "remote", "add", "upstream", original_url])
    subprocess.call(["git", "-C", "fork_repo", "fetch", "upstream"])

    stats = subprocess.check_output(["git", "-C", "fork_repo", "rev-list", "--left-right", "--count", "master...upstream/master"])
    ahead, behind = map(int, stats.decode().split())

    diff_stats = subprocess.check_output(["git", "-C", "fork_repo", "diff", "--stat", "master...upstream/master"])
    lines_added = sum(int(line.split()[0]) for line in diff_stats.decode().split('\n') if "insertion" in line)
    lines_removed = sum(int(line.split()[0]) for line in diff_stats.decode().split('\n') if "deletion" in line)

    amount_of_change = ahead + behind + lines_added + lines_removed

    subprocess.call(["rm", "-rf", "fork_repo"])
    subprocess.call(["rm", "-rf", "original_repo"])

    return amount_of_change

if __name__ == '__main__':
    get_forks()
