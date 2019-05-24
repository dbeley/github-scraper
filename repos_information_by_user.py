"""
Python script skeleton
"""
import os
import logging
import time
import argparse
import configparser
import pandas as pd
from github import Github
from tqdm import tqdm
from pathlib import Path

logger = logging.getLogger()
temps_debut = time.time()


def main():
    args = parse_args()

    config = configparser.ConfigParser()
    config.read("config.ini")
    username = config["github"]["username"]
    password = config["github"]["password"]
    export_filename_complete = "Exports/complete-user-repos.csv"

    if args.user:
        users = args.user.split(",")
    if args.file:
        with open(args.file, "r") as f:
            users = f.readlines()
        users = [x.strip() for x in users]
    else:
        users = [username]
    logger.debug("Users : %s", users)

    g = Github(username, password)

    dict_complete = {}
    for index_complete, user in enumerate(users, 1):
        logger.info("Extracting repos information of %s", user)

        dict_repos = {}
        user = g.get_user(user)
        repos = user.get_repos()
        for index, repo in tqdm(
            enumerate(repos, 1), total=user.public_repos, dynamic_ncols=True
        ):
            try:
                dict = {}
                dict["User"] = user.login
                logger.debug("User : %s", dict["User"])
                dict["Owner"] = repo.owner.login
                logger.debug("Owner : %s", dict["Owner"])
                dict["Name"] = repo.name
                logger.debug("Name : %s", dict["Name"])
                dict["URL"] = repo.html_url
                logger.debug("URL : %s", dict["URL"])
                dict["Description"] = repo.description
                logger.debug("Description : %s", dict["Description"])
                dict["Stars"] = repo.stargazers_count
                logger.debug("Stars : %s", dict["Stars"])
                dict["Watchers"] = repo.watchers_count
                logger.debug("Watchers : %s", dict["Watchers"])
                dict["Subscribers"] = repo.subscribers_count
                logger.debug("Subscribers : %s", dict["Subscribers"])
                dict["Forks"] = repo.forks_count
                logger.debug("Forks : %s", dict["Forks"])
                dict["Fork"] = repo.fork
                logger.debug("Fork : %s", dict["Fork"])
                try:
                    dict["License"] = repo.get_license().license.name
                except Exception as e:
                    logger.error(e)
                    dict["License"] = "NA"
                logger.debug("License : %s", dict["License"])
                dict["Language"] = repo.language
                logger.debug("Language : %s", dict["Language"])
                dict["Languages"] = repo.get_languages()
                logger.debug("Languages : %s", dict["Languages"])
                dict["Creation date"] = repo.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                logger.debug("Creation date : %s", dict["Creation date"])
                try:
                    dict["Modification date"] = repo.pushed_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    logger.debug(
                        "Modification date : %s", dict["Modification date"]
                    )
                except Exception as e:
                    logger.error(e)
                    dict["Modification date"] = "NA"
                try:
                    dict["Contributors"] = repo.get_contributors().totalCount
                    logger.debug("Contributors : %s", dict["Contributors"])
                except Exception as e:
                    logger.error(e)
                    dict["Contributors"] = "NA"
                dict["Topics"] = repo.get_topics()
                logger.debug("Topics : %s", dict["Topics"])
            except Exception as e:
                logger.error(e)

            dict_repos[index] = dict
            dict_complete[index_complete] = dict
            index_complete += 1

        Path("Exports").mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame.from_dict(dict_repos, orient="index")
        export_filename_user = f"Exports/{user.login}-repos.csv"
        df.to_csv(export_filename_user, sep="\t")
    if not os.path.isfile(export_filename_complete):
        df = pd.DataFrame.from_dict(dict_complete, orient="index")
        df.to_csv(export_filename_complete, sep="\t", header=True)
    else:
        with open(export_filename_complete, "a") as f:
            df = pd.DataFrame.from_dict(dict_complete, orient="index")
            df.to_csv(f, sep="\t", header=False)
    logger.info("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description="Repos information by user")
    parser.add_argument(
        "--debug",
        help="Display debugging information",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-u", "--user", help="Users to search (separated by comma)", type=str
    )
    parser.add_argument(
        "-f",
        "--file",
        help="File containing the users (one by line)",
        type=str,
    )
    parser.set_defaults(boolean_flag=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
