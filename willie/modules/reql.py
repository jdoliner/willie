"""
reql.py - ReQL Module
Copyright 2010, Michael Yanovich, yanovich.net
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""

import sandbox as s
import rethinkdb as r
import inspect

for k,v in inspect.getmembers(r.ast):
    if type(v) == type(type(1)):
        s.proxy.SAFE_TYPES += (v,)

cfg = s.SandboxConfig()
cfg.allowModule("rethinkdb", *dir(r))
box = s.Sandbox(cfg)

def eval_reql(string):
    import rethinkdb as r
    return eval(string)

def output_results(res, willie):
    if type(res) == r.Cursor:
        data = []
        for v, unused in zip(res, xrange(6)):
            data += [v]
        if len(data) > 5:
            willie.say(str(data)[:-1] + ",...]")
        else:
            willie.say(str(data))
    else:
        willie.say(str(res))


def reql(willie, trigger):
    """.reql <query> - Executes <query> as a piece of ReQL code (in python)."""
    if trigger.group(2) == " " or trigger.group(2) == "" or str(trigger.group(2)) == None or str(trigger.group(2)) == "" or trigger.group(2) == None:
        willie.say("I'm sorry, " + str(trigger.nick) + ", but you must enter a query.")
    else:
        query = box.call(eval_reql, trigger.group(2))
        c = r.connect()
        res = query.run(c)
        output_results(res, willie)
        c.close()

reql.commands = ['reql']
reql.priority = 'medium'

if __name__ == '__main__':
    print __doc__.strip()

