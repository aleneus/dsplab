import json
from dsplab.flow.plan import get_plan_from_dict

with open('plan.json') as buf:
    conf = json.loads(buf.read())

p = get_plan_from_dict(conf)

x = 1
y = p([x, ])
print(y)
