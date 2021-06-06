from datetime import datetime, timedelta

from dotenv import load_dotenv

import os

from github import Github


load_dotenv('.env')

TIMEDELTA = timedelta(hours=1)
MIN_PYTHON_LOC = 10
MIN_PYTHON_PERC = 0.5


def main():
    # using an access token
    g = Github(os.environ.get("GH_ACCESS_TOKEN"))

    end_date = datetime.utcnow()
    start_date = end_date - TIMEDELTA
    results = True

    while results:
        q = (f"size:<10000 "
             f"language:python "
             f"created:{start_date.strftime('%Y-%m-%dT%H:%M:%S')}..{end_date.strftime('%Y-%m-%dT%H:%M:%S')}")
        print(q)
        repositories = g.search_repositories(q)
        print("Total count:", repositories.totalCount)
        results = repositories.totalCount
        for repo in repositories:
            languages = repo.get_languages()
            if "Python" not in languages and languages["Python"] < MIN_PYTHON_LOC:
                continue
            python_num_lines = languages["Python"]
            other_lang_num_lines = sum(num_lines for lang, num_lines in languages.items() if lang != "Python")
            perc_python = python_num_lines / (python_num_lines + other_lang_num_lines)
            if perc_python < MIN_PYTHON_PERC:
                continue

            os.system(f"git clone {repo.clone_url} repos/{repo.full_name}")
        end_date -= TIMEDELTA
        start_date -= TIMEDELTA


if __name__ == '__main__':
    main()