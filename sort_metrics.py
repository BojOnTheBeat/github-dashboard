from github import Github
import os


def get_repos_for_org(org):
    # (Str) -> Iterator[Repo] 
    github_client = Github(os.environ["GITHUB_TOKEN"])
    org = github_client.get_organization(str(org))

    return org.get_repos()

def get_sort_function_from_sort_metric(sort_by):
    # (Str) -> Function
    return SORT_METRICS[sort_by]

def sort_by_stars(repos, lim=10):
    # (Iterator[Repo]) -> Iterator[Repo]
    return sorted(repos, key=lambda x: x.stargazers_count, reverse=True)[:lim]

def sort_by_forks(repos, lim=10):
    # (Iterator[Repo]) -> Iterator[Repo]
    return sorted(repos, key=lambda x: x.forks_count, reverse=True)[:lim]

def sort_by_contributors(repos, lim=10):
    # (Iterator[Repo]) -> Iterator[Repo]

    # get list of contributors then count it.
    return sorted(repos, key=get_num_contributors, reverse=True)[:lim]

def get_num_contributors(repo):
    # (Repo) -> Int
    return repo.get_contributors().totalCount

SORT_METRICS = {
    'Stars': sort_by_stars,
    'Forks': sort_by_forks,
    'Contributors': sort_by_contributors
}