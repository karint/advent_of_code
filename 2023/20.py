"""
Part 1:
Send pulses through a series of modules by pressing a button.

Part 2:
Determine how many button presses is needed to send a low pulse signal
to a given target.
"""
import math
import os

from collections import defaultdict
from util import run


class Status:
    OFF = 'off'
    ON = 'on'


class PulseType:
    LOW = 'low'
    HIGH = 'high'

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
        self.status = Status.OFF
        self.targets = targets

    def __repr__(self):
        return '%' + self.id

    def send(self, pulse_queue):
        for t in self.targets:
            pulse_queue.append((self.id, t, PulseType.LOW if self.status == Status.OFF else PulseType.HIGH))

    def receive(self, from_, pulse, pulse_queue):
        if pulse == PulseType.LOW:
            self.status = Status.OFF if self.status == Status.ON else Status.ON
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
        self.queued_pulse = (
            PulseType.LOW if all(last == PulseType.HIGH for last in self.most_recents.values())
            else PulseType.HIGH
        )
        self.send(pulse_queue)


BROADCASTER = 'broadcaster'
FLIPFLOP_PREFIX = '%'
CONJ_PREFIX = '&'

PREFIX_TO_CLASS = {
    FLIPFLOP_PREFIX: FlipFlopModule,
    CONJ_PREFIX: ConjModule,
}


def get_modules(lines):
    modules = {}
    conj_ids = set()
    for line in lines:
        line = line.strip()
        module, targets = line.split(' -> ')
        targets = targets.split(', ')

        if module == BROADCASTER:
            modules[BROADCASTER] = BroadcastModule(BROADCASTER, targets)
        else:
            prefix, id_ = module[0], module[1:]
            modules[id_] = PREFIX_TO_CLASS[prefix](id_, targets)
            if prefix == CONJ_PREFIX:
                conj_ids.add(id_)

    # Initialize most recent inputs for all conjunction nodes to low
    for module in modules.values():
        for t in module.targets:
            if t in conj_ids:
                modules[t].most_recents[module.id] = PulseType.LOW

    return modules


def part_1(lines):
    modules = get_modules(lines)

    pulse_counts = defaultdict(int)
    for _ in range(1000):
        pulse_queue = []
        pulse_counts[PulseType.LOW] += 1
        modules[BROADCASTER].receive('button', PulseType.LOW, pulse_queue)

        while pulse_queue:
            new_pulse_queue = []
            for source, target, pulse in pulse_queue:
                pulse_counts[pulse] += 1
                if target in modules:
                    modules[target].receive(source, pulse, new_pulse_queue)
            pulse_queue = new_pulse_queue

    return pulse_counts[PulseType.HIGH] * pulse_counts[PulseType.LOW]


def part_2(lines):
    modules = get_modules(lines)

    # To find a cycle length, get the first two times each of these sends
    # a high pulse. ulled these by looking at the file. rs needs hj to send
    # a low pulse, meaning all inputs into hj need to be high on the
    # same button press. Those inputs are ks, jf, qs, and zk.
    need_high_pulse = {
        'ks': [],
        'jf': [],
        'qs': [],
        'zk': [],
    }
    presses = 0
    while any(len(highs) < 2 for highs in need_high_pulse.values()):
        presses += 1
        pulse_queue = []
        modules['broadcaster'].receive('button', PulseType.LOW, pulse_queue)

        while pulse_queue:
            new_pulse_queue = []
            for source, target, pulse in pulse_queue:
                if source in need_high_pulse and pulse == PulseType.HIGH:
                    if (
                        not need_high_pulse[source] or
                        (len(need_high_pulse[source]) < 2 and need_high_pulse[source][-1] != presses)
                    ):
                        need_high_pulse[source].append(presses)
                if target in modules:
                    modules[target].receive(source, pulse, new_pulse_queue)
            pulse_queue = new_pulse_queue

    return math.lcm(*(highs[1] - highs[0] for highs in need_high_pulse.values()))


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)
