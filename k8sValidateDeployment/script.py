#!/usr/bin/python3
import argparse
import json
import subprocess
import sys
import time
import logging
from pprint import pprint

logging.basicConfig(level=logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(description='Trigger Git Hub action and monitor')
    parser.add_argument('-a', '--app', help='app name', required=True)
    parser.add_argument('-g', '--gitsha', help='github sha', required=True)
    parser.add_argument('-s', '--time_sleep', help='sleep time', required=False)
    parser.add_argument('-m', '--max_attempt', help='max attempt', required=False)
    return vars(parser.parse_args())

#.items[] | select(.metadata.labels.app  | contains("adapter"))
def find_images(app_name):
    apps = []
    actual_json = json.loads(subprocess.check_output("kubectl get pods -o json", shell=True))
    for item in actual_json['items']:
        if item['metadata']['labels']['app'] == app_name:
            apps.append(item)
    return apps


def find_shas(images):
    actual_git_shas = []
    for image in images:
        for container in image['spec']['containers']:
            image_value = container['image']
            actual_git_shas.append(image_value.split(':', 1)[1])
    return actual_git_shas


def is_sha_updated(element_list, expected_sha):
    result = False
    if len(element_list) > 0:
        all_sha_are_same = all(elem == element_list[0] for elem in element_list)
        if all_sha_are_same:
            if expected_sha in element_list:
                print("GitSha, '{}' found in List : {}".format(expected_sha, element_list))
                result = True
            else:
                print("Expected Sha {} is not Deployed yet, current deployed shas: {}".format(expected_sha, element_list))
        else:
            print("All Elements in List are Not Equal")
    return result


def validate_shas_are_updated(app_name, git_sha, max_attempt=100, sleep_duration=5):
    counter = 1
    shas_deployed = False
    while counter <= max_attempt:
        images = find_images(app_name)
        actual_git_sha = find_shas(images)
        shas_deployed = is_sha_updated(actual_git_sha, git_sha)
        if shas_deployed:
            print("All git shas has been updated")
            break
        counter += 1
        time.sleep(sleep_duration)
    return shas_deployed


def assert_exit(condition, err_message):
    try:
        assert condition
    except AssertionError:
        sys.exit(err_message)

def main():
    args = parse_args()
    app_name = args['app']
    logging.info(f"App arg {app_name}")
    expected_sha = args['gitsha']
    logging.info(f"Expected sha {app_name}")
    max_attempt = int(args['max_attempt'])
    sleep_duration = int(args['time_sleep'])
    shas_deployed = validate_shas_are_updated(app_name, expected_sha, max_attempt, sleep_duration)
    assert_exit(shas_deployed, "Failed to update shas after specified time")


if __name__ == '__main__':
    main()