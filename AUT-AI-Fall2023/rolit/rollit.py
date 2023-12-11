import argparse
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

from Agents import *
from Display import *
from multiAgents import *
from Game import *
from util import *

from typing import List

def readCommand(argv):
    """
    Processes the command used to run pacman from the command line.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--question', nargs='?', choices=['q1', 'q2', 'q3', 'q4'])

    parser.add_argument('-n', '--players', choices=[2, 4], type=int, default=2)

    parser.add_argument('-a', '--main-agent', nargs='?', default='MouseAgent')

    parser.add_argument('-d', '--own-depth', nargs='?', type=int, default=2)

    parser.add_argument('-fn', '--evaluation-function', nargs='?', choices=['scoreEvaluationFunction', 'betterEvaluationFunction'], default='scoreEvaluationFunction')

    parser.add_argument('-ea', '--opponents-agent', nargs='?', default='PartiallyRandomAgent')

    parser.add_argument('-ed', '--opponents-depth', nargs='?', type=int, default=1)

    parser.add_argument('-ec', '--opponents-config', nargs='*')

    parser.add_argument('-ds', '--display-setting', nargs='?', choices=['graphic', 'console', 'minimal'], default='graphic')

    parser.add_argument('-ws', '--window-size', nargs='?', type=int, default=800)

    parser.add_argument('-l', '--load', nargs='?')

    args = parser.parse_args(argv)

    return args

def get_display(args):

    if args['display_setting'] == 'graphic':
        display = globals()['GraphicalDisplay'](args['window_size'])
    elif args['display_setting'] == 'console':
        display = globals()['ConsoleDisplay']()
    elif args['display_setting'] == 'minimal':
        display = globals()['Display']()

    return display

def get_agents(args):

    own_dict = {'depth': args['own_depth'], 'evalFn': args['evaluation_function'], 'window_size': args['window_size']}
    opp_dict = {'depth': args['opponents_depth'], 'window_size': args['window_size']}
    
    if args['main_agent'] == 'MouseAgent':
        if args['display_setting'] != 'graphic':
            print('you can only use the MouseAgent with GraphicalDisplay.')
            exit(-1)
        else:
            my_agent = globals()['MouseAgent'](0, **own_dict)
    else:
        my_agent = globals()[args['main_agent']](0, **own_dict)

    agents = [my_agent]

    opponents_count = args['players'] - 1

    if isinstance(args['opponents_config'], List) and len(args['opponents_config']) >= opponents_count:

        for i, config in enumerate(args['opponents_config'], start=1):
            agents.append(globals()[config](i, **opp_dict))

    else:

        agent_class = globals()[args['opponents_agent']]
        for i in range(1, opponents_count + 1):
            agents.append(agent_class(i, **opp_dict))

    return agents

def get_state(args):

    if args['load']:

        try:
            with open(args['load'], 'rb') as f:
                state = pickle.load(f)

            if not isinstance(state, GameState):
                raise Exception('wrong serialized object.')

        except Exception as e:
            print('there was something wrong with your GameState save.')
            exit(-1)
    
    else:
        state = GameState()
        state.initialize(args['players'])

    return state

import sys
if __name__ == "__main__":

    args = readCommand(sys.argv[1:])

    modes = load_modes('modes.pickle')

    if args.question:
        if modes and args.question in modes:
            args = modes[args.question]
        else:
            print('wrong pickle file or wrong game mode!')
            exit(-1)
    else:
        args = args.__dict__
    
    agents = get_agents(args)
    display = get_display(args)
    state = get_state(args)

    game = Game(agents, display, state)
    game.run()
    
    