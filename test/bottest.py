# Main file for bot pytest actions. Uses dpytest to test bot activity on a simulated server with simulated members
import discord
import os
from datetime import datetime, timedelta

import discord.ext.test as dpytest
from dotenv import load_dotenv

import pytest


# TODO Test user join messages
# Tests cogs/hello.py
@pytest.mark.asyncio
async def test_hello(bot):
    await dpytest.message("$hello")
    assert dpytest.verify().message().content("Hello World!")


# Tests cogs/ping.py
@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("$ping")
    assert dpytest.verify().message().contains().content("Pong!")


# Tests on_member_join events
@pytest.mark.asyncio
async def test_join(bot):
    config = dpytest.RunnerConfig
    await dpytest.member_join(name="Bongus1")
    await dpytest.member_join(name="Bongus2")
    print(f'\n{bot.guilds}\n')
    print(f'\n{dpytest.RunnerConfig.members}\n')
    # await dpytest.message("$join group 1")

# Tests cogs/deadline.py
@pytest.mark.asyncio
async def test_deadline(bot):
    # Clear our reminders: Only if testing fails and leaves a reminders.JSON file with values behind
    # await dpytest.message("$clearreminders")
    # assert dpytest.verify().message().contains().content("All reminders have been cleared..!!")
    # Test reminders while none have been set
    await dpytest.message("$coursedue CSC505")
    assert dpytest.verify().message().content("Rejoice..!! You have no pending homeworks for CSC505..!!")
    # Test setting 1 reminder
    await dpytest.message("$addhw CSC505 DANCE SEP 21 2050 10:00")
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC505 homework named: DANCE which is due on: 2050-09-21 10:00:00")
    # Test setting a 2nd reminder
    await dpytest.message("$addhw CSC510 HW1 DEC 21 2050 19:59")
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC510 homework named: HW1 which is due on: 2050-12-21 19:59:00")
    # Test deleting reminder
    await dpytest.message("$deleteReminder CSC510 HW1")
    assert dpytest.verify().message().content(
        "Following reminder has been deleted: Course: CSC510, Homework Name: HW1, Due Date: 2050-12-21 19:59:00")
    # Test re-adding a reminder
    await dpytest.message("$addhw CSC510 HW1 DEC 21 2050 19:59")
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC510 homework named: HW1 which is due on: 2050-12-21 19:59:00")
    # Test listing multiple reminders
    await dpytest.message("$listreminders")
    assert dpytest.verify().message().contains().content(
        "CSC505 homework named: DANCE which is due on: 2050-09-21 10:00:00")
    assert dpytest.verify().message().contains().content(
        "CSC510 homework named: HW1 which is due on: 2050-12-21 19:59:00")
    # Test $coursedue
    await dpytest.message("$coursedue CSC505")
    assert dpytest.verify().message().contains().content(
        "DANCE is due at 2050-09-21 10:00:00")
    # Try to change the due date of DANCE to something impossible
    await dpytest.message("$changeduedate CSC505 DANCE 4")
    assert dpytest.verify().message().contains().content(
        "Due date could not be parsed")
    # Try adding a reminder due in an hour
    now = datetime.now() + timedelta(hours=1)
    dt_string = now.strftime("%b %d %Y %H:%M")
    await dpytest.message(f'$addhw CSC600 HW0 {dt_string}')
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC600 homework named: HW0")
    # Check to see that the reminder is due this week
    await dpytest.message("$duethisweek")
    assert dpytest.verify().message().contains().content("CSC600 HW0 is due this week")
    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("$clearreminders")
    assert dpytest.verify().message().contains().content("All reminders have been cleared..!!")