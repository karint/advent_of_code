"""
Part 1:
Part 2:
"""
import math
import os

from collections import defaultdict
from util import run


class BroadcastModule:
    def __init__(self, id_, targets):
        self.id = id_
        self.last_pulse = None
        self.targets = targets

    def __repr__(self):
        return 'broadcast'

    def send(self, pulse_queue):
        for t in self.targets:
            pulse_queue.append(((self.id, t, self.last_pulse)))

    def receive(self, from_, pulse, pulse_queue):
        self.last_pulse = pulse
        self.send(pulse_queue)


class FlipFlopModule:
    def __init__(self, id_, targets):
        self.id = id_
        self.status = 'off'
        self.targets = targets

    def __repr__(self):
        return '%' + self.id

    def send(self, pulse_queue):
        if self.status == 'off':
            for t in self.targets:
                pulse_queue.append((self.id, t, 'low'))
        elif self.status == 'on':
            for t in self.targets:
                pulse_queue.append((self.id, t, 'high'))

    def receive(self, from_, pulse, pulse_queue):
        if pulse == 'high':
            pass
        else:
            self.status = 'off' if self.status == 'on' else 'on'
            self.send(pulse_queue)


class ConjModule:
    def __init__(self, id_, targets):
        self.id = id_
        self.targets = targets
        self.most_recents = {}
        self.queued_pulse = None

    def __repr__(self):
        return '&' + self.id

    def send(self, pulse_queue):
        pulse = self.queued_pulse
        for t in self.targets:
            pulse_queue.append((self.id, t, self.queued_pulse))

    def receive(self, from_, pulse, pulse_queue):
        self.most_recents[from_] = pulse
        self.queued_pulse = 'low' if all(last == 'high' for last in self.most_recents.values()) else 'high'
        self.send(pulse_queue)
        # print('recents now', self.most_recents)


def part_1(lines):
    modules = {}
    conj_ids = set()
    broadcaster = None
    for line in lines:
        line = line.strip()
        module, targets = line.split(' -> ')
        targets = targets.split(', ')
        if module == 'broadcaster':
            broadcaster = BroadcastModule('broadcaster', targets)
            modules[module] = broadcaster
        elif module.startswith('%'):
            modules[module[1:]] = FlipFlopModule(module[1:], targets)
        elif module.startswith('&'):
            modules[module[1:]] = ConjModule(module[1:], targets)
            conj_ids.add(module[1:])

    for module in modules.values():
        for t in module.targets:
            if t in conj_ids:
                modules[t].most_recents[module.id] = 'low'

    pulse_counts = defaultdict(int)
    for _ in range(1000):
        pulse_queue = []
        pulse_counts['low'] += 1
        broadcaster.receive('button', 'low', pulse_queue)

        while pulse_queue:
            new_pulse_queue = []
            for source, target, pulse in pulse_queue:
                print('%s -%s-> %s' % (source, pulse, target))
                if source in conj_ids:
                    print(modules[source].most_recents)
                pulse_counts[pulse] += 1
                if target in modules:
                    modules[target].receive(source, pulse, new_pulse_queue)
            pulse_queue = new_pulse_queue

    print(pulse_counts)

    return pulse_counts['high'] * pulse_counts['low']


def part_2(lines):
    TARGET = 'rx'

    modules = {}
    conj_ids = set()
    broadcaster = None
    for line in lines:
        line = line.strip()
        module, targets = line.split(' -> ')
        targets = targets.split(', ')
        if module == 'broadcaster':
            broadcaster = BroadcastModule('broadcaster', targets)
            modules[module] = broadcaster
        elif module.startswith('%'):
            modules[module[1:]] = FlipFlopModule(module[1:], targets)
        elif module.startswith('&'):
            modules[module[1:]] = ConjModule(module[1:], targets)
            conj_ids.add(module[1:])

    for module in modules.values():
        for t in module.targets:
            if t in conj_ids:
                modules[t].most_recents[module.id] = 'low'

    # For rx to get a single low pulse, all flip-flop switches upstream
    # need to be high on the same turn. We therefore calculate how many pulses it takes each
    # switch to send a high pulse.

    """
    rx: &hj
    &hj: &ks,&jf,&qs,&zk
    &jf: &rt
    &qs: &fv
    &ks: &sl
    &zk: &gk
    &rt: %bs,%pn,%vm,%vj,%zz,%bt,%jg,%rr,%mk
    &fv: %cn,%bc,%kp,%jr,%gn,%jx,%pq,%bf
    &sl: %rq,%dc,%ql,%jl,%mr,%jc,%gv,%mm,%cc
    &gk: %sb,%vz,%rk,%bz,%rl,%rh,%lg
    """

    all_need_high = {
        'ks': [],
        'jf': [],
        'qs': [],
        'zk': [],
    }

    presses = 0
    while any(len(highs) < 3 for highs in all_need_high.values()):
        presses += 1
        pulse_queue = []
        broadcaster.receive('button', 'low', pulse_queue)

        while pulse_queue:
            new_pulse_queue = []
            for source, target, pulse in pulse_queue:
                if source in all_need_high and pulse == 'high':
                    # Nothing recorded yet, record
                    if not all_need_high[source]:
                        all_need_high[source].append(presses)
                    elif len(all_need_high[source]) < 3 and all_need_high[source][-1] != presses:
                        all_need_high[source].append(presses)
                if target in modules:
                    modules[target].receive(source, pulse, new_pulse_queue)
            pulse_queue = new_pulse_queue

    high_cycle_lengths = []
    for key, highs in all_need_high.items():
        print(key, highs, highs[1] - highs[0])
        high_cycle_lengths.append(highs[1] - highs[0])

    return math.lcm(*high_cycle_lengths)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)
