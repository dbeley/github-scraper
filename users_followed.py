import argparse
import calendar
import configparser
import logging
import time
import pandas as pd
from github import Github
from pathlib import Path

logger = logging.getLogger()
temps_debut = time.time()


def check_ratelimit(github):
    core_rate_limit = github.get_rate_limit().core
    if core_rate_limit.remaining < 500:
        reset_timestamp = calendar.timegm(core_rate_limit.reset.timetuple())
        sleep_time = (
            reset_timestamp - calendar.timegm(time.gmtime()) + 5
        )  # add 5 seconds to be sure the rate limit has been reset
        logger.info(
            f"{core_rate_limit.remaining} remaining API calls. Waiting for {sleep_time} seconds."
        )
        time.sleep(sleep_time)


def create_record(user):
    return {
        "username": user.login,
        "url": user.html_url,
        "bio": user.bio,
        "blog": user.blog,
        "company": user.company,
        "created_at": user.created_at,
        "email": user.email,
        "followers": user.followers,
        "following": user.following,
        "id": user.id,
        "location": user.location,
        "name": user.name,
        "public_gists": user.public_gists,
        "public_repos": user.public_repos,
        "role": user.role,
        "site_admin": user.site_admin,
        "twitter_username": user.twitter_username,
        "updated_at": user.updated_at,
    }


def main():
    args = parse_args()

    config = configparser.ConfigParser()
    config.read("config.ini")
    username = config["github"]["username"]
    token = config["github"]["token"]

    g = Github(token)
    check_ratelimit(g)
    if args.user:
        list_users = args.user.split(",")
    else:
        list_users = [username]

    Path("Exports").mkdir(parents=True, exist_ok=True)
    for username in list_users:
        github_user = g.get_user(username)
        list_following = github_user.get_following()
        list_dict = []
        check_ratelimit(g)
        for user in list_following:
            list_dict.append(create_record(user))
            if args.extended:
                check_ratelimit(g)
                for followed_user in user.get_following():
                    list_dict.append(create_record(followed_user))

        export_filename = (
            f"Exports/{int(time.time())}_{github_user.login}-following.csv"
            if not args.extended
            else f"Exports/{int(time.time())}_{github_user.login}-following_extended.csv"
        )
        with open(export_filename, "w") as f:
            df = pd.DataFrame(list_dict).drop_duplicates()
            df.to_csv(f, sep="\t", header=True, index=False)

    logger.info("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get the users followed by another user"
    )
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
        "-e",
        "--extended",
        help="Extract not only followers infos, but follower's followers infos too.",
        dest="extended",
        action="store_true",
    )
    parser.set_defaults(extended=False)
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
