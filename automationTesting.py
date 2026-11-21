import requests
import sys
import re

BASE_URL = "http://localhost:3000"

passed = 0
failed = 0


def check(name, condition):
    global passed, failed

    if condition:
        print(f"[PASS] {name}")
        passed += 1
    else:
        print(f"[FAIL] {name}")
        failed += 1


print("\n--- Eisenhower Todo Automated Testing ---\n")


# TEST 1: Home page
try:
    response = requests.get(BASE_URL + "/")

    check(
        "GET / - Home page",
        response.status_code == 200
    )

except Exception as e:
    print("[FAIL] Server connection:", e)
    sys.exit(1)


# TEST 2: Add Task page
response = requests.get(BASE_URL + "/tasks/new")

check(
    "GET /tasks/new - Add task page",
    response.status_code == 200
)


# TEST 3: Create a task
task_title = "Automation Test Task"

task_data = {
    "title": task_title,
    "description": "Created automatically by automationTesting.py",
    "isUrgent": "on",
    "isImportant": "on"
}

response = requests.post(
    BASE_URL + "/tasks",
    data=task_data,
    allow_redirects=True
)

check(
    "POST /tasks - Create task",
    response.status_code == 200
    and task_title in response.text
)


# TEST 4: Reject empty title
response = requests.post(
    BASE_URL + "/tasks",
    data={"title": ""},
    allow_redirects=False
)

check(
    "POST /tasks - Reject empty title",
    response.status_code == 400
)


# TEST 5: Delete the task we just created

home_response = requests.get(BASE_URL + "/")

# Find all delete URLs present on the page
delete_urls = re.findall(
    r'action="(/tasks/[a-fA-F0-9]{24}/delete)"',
    home_response.text
)

if delete_urls:

    # The newly created task appears first because
    # MongoDB tasks are sorted by createdAt descending
    delete_url = delete_urls[0]

    delete_response = requests.post(
        BASE_URL + delete_url,
        allow_redirects=True
    )

    check(
        "POST /tasks/:id/delete - Delete task",
        delete_response.status_code == 200
    )

else:

    print("[DEBUG] Could not find any delete URL in homepage HTML")

    check(
        "POST /tasks/:id/delete - Delete task",
        False
    )


# FINAL RESULT

print("\n--------------------------------")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("--------------------------------\n")


if failed > 0:
    sys.exit(1)

print("All automated tests passed!")