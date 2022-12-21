import subprocess
import time
from enum import Enum
import requests

BASE_URL = "http://127.0.0.1:8000"
ATTACKS_URL = BASE_URL + "/attacks/api"


class AttackStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    DONE = "done"


def get_next_attack():
    try:
        response = requests.get(ATTACKS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.ConnectionError:
        print(f'No connection to server: {ATTACKS_URL}')
        return None


def get_attack(attack_id):
    print(f'getting attack with id: {attack_id}, url: {ATTACKS_URL}')
    response = requests.get(ATTACKS_URL, params={'attack_id': attack_id})
    print(f'response: {response}')
    if response.status_code == 200:
        return response.json()
    else:
        return None


def update_attack_status(attack, status):
    response = requests.post(ATTACKS_URL, data={'attack_id': attack['id'], 'status': status})
    if response.status_code == 204:
        return True
    else:
        return False


def execute_attack_async(attack):
    print("Executing attack: " + attack['name'])
    return subprocess.Popen(attack['command'], shell=True)


def execute_attack_and_poll(attack):
    p = execute_attack_async(attack)
    while True:
        try:
            time.sleep(5)
            if p.poll() is not None:
                break
            attack_id_ = attack['id']
            attack = get_attack(attack_id_)
            if attack['status'] == AttackStatus.STOPPED.value:
                print("Stopping attack: " + attack['name'])
                p.terminate()
                return False
            else:
                print(f'still running attack: {attack_id_}')
        except requests.exceptions.ConnectionError:
            print(f'No connection to server: {ATTACKS_URL}')
    return True


def main():
    print("Starting attack bot")
    while True:
        print("Polling for next attack")
        attack = get_next_attack()
        if attack is not None:
            print("Found attack: " + attack['name'])
            update_attack_status(attack, AttackStatus.RUNNING.value)
            run_status = execute_attack_and_poll(attack)
            if run_status:
                print("Attack completed: " + attack['name'])
                update_attack_status(attack, AttackStatus.DONE.value)
        else:
            print("No attacks to execute")
            time.sleep(5)


if __name__ == "__main__":
    main()
