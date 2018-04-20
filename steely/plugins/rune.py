'''buenos dias'''


__author__ = 'iandioch'
COMMAND = 'rune'

NORMAL = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
RUNE = '🜣🜖🝔🜵🞌🝗🜶🜘🜶🜶🝁🜾🝀🝀🜃🜵🜣🜛🜖🜟🜫🜾🝁🝖🜞🜖🜺🜾🜴🜃🜵🝞🜶🝔🝁🜖🜴🝔🜾🝁🝳🜵🜃🜾🝗🜶🝁🞌🝀🜣🜶🜶🝁'

# 🜾🜴🜃🜖🝞🜶🝞🜖🝀🜖🜞🜶🜟🜾🜵🝞🜣🝞🜵🜼🜶🝀🜃🜵🜣🜹🜟🜾🝖🜘🜶🜵🜃🜾🝗🜶🝁🞌🝀🜘🜶🜶🝁🜫🜾🝖🜵🝁🝊🜶🝁🜖🜨🝊🜃🜾🝀🝀🜶🝁🝀🜵🜖🝁🜹🜘🜨🝀🜵🝳🜶🜛🜵🝳🜶🝳🜵🞌🝳🜴🜺🜵🝀🜶🜖🝁🜶🝔🜣🜵🝁🜛🜶🜵🜃🜾🝗🜶🝁🞌🝀🝳🜖🝁🜶🜣🜖🝔🝖🜶🝀🝔🜾🝁🝳🜾🜟🝀🜃🜶🜺🜶🜞🜖🜺🜶🜫🜾🜺🝀🜖🜞🝀🜃🜶🜫🜺🜖🜘🝞🜶🜟🜹🜾🝁🝖🜴🜾🝖🝔🝀🜃🜾🝁🜼🜣🜞🜖🜺🜺🜶🜾🝳🜵🝁🝊🝔🜾🝁🝳🜛🜖🝁🝊🜺🜾🝀🜣🜞🜖🜺🝳🜶🜛🜖🝳🜵🝁🝊🝒🜺🜶🝞🜾🝀🜶🝳🝐🜃🜾🜾🝁🝖🜖🝁🜶🜴🜺🜵🝀🝀🜶🝁🜾🜣🝀🜾🝀🜵🜣🝀🜵🜛🜾🝞🝳🜶🜛🜖🝳🜶🜺🜞🜖🜺🜛🜵🜫🜃🜶🜺🝀🜶🜠🝀🜣🜖🜞🝀🜃🜵🜣🝁🜾🝀🜨🜺🜶🝯'

FROM = NORMAL + RUNE
TO = RUNE + NORMAL
RUNE_TRANS = str.maketrans(FROM, TO)


def ruin(string):
    return string.translate(RUNE_TRANS)


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    message = bot.fetchThreadMessages(thread_id=thread_id, limit=2)[1]
    bot.sendMessage(ruin(message.text), thread_id=thread_id,
                    thread_type=thread_type)

if __name__ == '__main__':
    print(ruin('hey now you\'re an all star'))
    print(ruin("🜘🞌🜞 🝀🜃🝁 🜞🜃🜫'🜛🞌 🜣🝀 🜣🜾🜾 🜖🜟🜣🜛"))  # gibberish on purpose yo
