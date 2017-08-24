#!/usr/bin/env python3


from contextlib import suppress
from fbchat import log, Client
from tinydb import TinyDB
from vapor import vapor
from utils import list_plugins
import config
import imp
import os
import random
import requests
import spell
import sys
import threading


CMD_DB = TinyDB('quote.json')
HELP_DOC = '''help <command>

help syntax:
optinal arguments: [arg name]
mandatory arguments: <arg name>
literal arguments: `this|yesterday|tomorrow`

literal commands can be mandatory or optional'''


class SteelyBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_suggestions = {}
        self.load_plugins()

    def load_plugins(self):
        self.non_plugins = []
        self.plugins = {}
        self.plugin_helps = {
            '.help': HELP_DOC
        }
        for plugin in list_plugins():
            if plugin.__doc__:
                self.plugin_helps[plugin.COMMAND.lower()] = plugin.__doc__.strip('\n')
            if plugin.COMMAND:
                self.plugins[plugin.COMMAND.lower()] = plugin
            else:
                self.non_plugins.append(plugin)
        spell.WORDS = self.plugins.keys()

    def send_command(self, author_id, message, thread_id, thread_type, **kwargs):
        # run plugins that have a command
        if " " in message:
            command, message = message.split(' ', 1)
        else:
            command, message = message, ""
        command = command.lower().strip()
        if not command in self.plugins:
            suggestions = list(enumerate(spell.correction(command)))
            if not suggestions:
                return
            if len(suggestions) == 1:
                command = suggestions[0][1]
            else:
                self.sendMessage('type the number to correct\n' +
                        ", ".join("{}: {}".format(n, suggestion) for n, suggestion in suggestions),
                        thread_id=thread_id, thread_type=thread_type)
                self.last_suggestions = suggestions
                self.last_message = message
                return
        plugin = self.plugins[command]
        thread = threading.Thread(target=plugin.main,
            args=(self, author_id, message, thread_id, thread_type), kwargs=kwargs)
        thread.deamon = True
        thread.start()

    def onEmojiChange(self, author_id, new_emoji, thread_id, thread_type, **kwargs):
        nose = '👃'
        if new_emoji != nose:
            self.changeThreadEmoji(nose, thread_id=thread_id)

    def onNicknameChange(self, mid, author_id, changed_for, new_nickname, thread_id, thread_type, ts, metadata, msg):
        self.changeNickname(vapor(new_nickname), user_id=changed_for, thread_id=thread_id, thread_type=thread_type)

    def onFriendRequest(self, from_id, msg):
        self.friendConnect(from_id)

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        if author_id == self.uid:
            return

        # run plugins that have no command
        for plugin in self.non_plugins:
                thread = threading.Thread(target=plugin.main,
                    args=(self, author_id, message, thread_id, thread_type), kwargs=kwargs)
                thread.deamon = True
                thread.start()

        if message.isdigit():
            for number, suggestion in self.last_suggestions:
                if number == int(message):
                    message = suggestion + " " + self.last_message
                    self.send_command(author_id, message, thread_id, thread_type, **kwargs)
                    self.last_message = ""
                    self.last_suggestions = []
                    return

        if not message.startswith("."):
            return

        self.send_command(author_id, message, thread_id, thread_type, **kwargs)


if __name__ == '__main__':
    client = SteelyBot(config.EMAIL, config.PASSWORD)
    while True:
        with suppress(requests.exceptions.ConnectionError):
            client.listen()