"""
reql.py - ReQL Module
Copyright 2010, Michael Yanovich, yanovich.net
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""

import sandbox as s
import rethinkdb as r

s.proxy.SAFE_TYPES += (type(r.expr(1)),)

cfg = s.SandboxConfig()
cfg.allowModule("rethinkdb", *dir(r))
box = s.Sandbox(cfg)


def eval_reql(string):
    import rethinkdb as r
    return eval(string)

def reql(willie, trigger):
    """.reql <query> - Executes <query> as a piece of ReQL code (in python)."""
    if trigger.group(2) == " " or trigger.group(2) == "" or str(trigger.group(2)) == None or str(trigger.group(2)) == "" or trigger.group(2) == None:
        willie.say("I'm sorry, " + str(trigger.nick) + ", but you must enter a query.")
    else:
        query = box.call(eval_reql, trigger.group(2))
        c = r.connect()
        willie.say(str(query.run(c)))
        c.close()

reql.commands = ['reql']
reql.priority = 'medium'

if __name__ == '__main__':
    print __doc__.strip()

