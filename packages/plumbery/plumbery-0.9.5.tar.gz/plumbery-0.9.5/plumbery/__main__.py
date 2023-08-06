# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import logging
import argparse
import sys

from plumbery.engine import PlumberyEngine
from plumbery import __version__
from plumbery.logging import setup_logging
log = setup_logging()


def parse_args(args=[]):
    """
    Guesses the intention of the runner of this program

    :param args: arguments to be considered for this invocation
    :type args: a list of ``str``

    You have to run the following command to know more::

        $ python -m plumbery fittings.yaml -h

    """

    parser = argparse.ArgumentParser(
        prog='python -m plumbery',
        description='Plumbing infrastructure with Apache Libcloud.',
        epilog='example: python -m plumbery fittings.yaml build')

    parser.add_argument(
        'fittings',
        nargs=1,
        help="File that is containing fittings plan, or '-' to read stdin")

    parser.add_argument(
        'action',
        nargs=1,
        help="An action, or a polisher: 'deploy', 'refresh', dispose', "
             "'secrets', 'build', 'configure', 'start', 'prepare', "
             "'information', 'ping', 'inventory', 'ansible', "
             "'stop', 'wipe', 'destroy'")

    parser.add_argument(
        'tokens',
        nargs='*',
        help="One blueprint, or several, e.g., 'web' or 'web sql'."
             "If omitted, all blueprints will be considered. "
             "Zero or more locations, e.g., '@NA12'. "
             "If omitted, all locations will be considered.",
        default=None)

    parser.add_argument(
        '-p', '--parameters',
        help='Parameters for this fittings plan')

    parser.add_argument(
        '-s', '--safe',
        help='Safe mode, no actual change is made to the infrastructure',
        action='store_true')

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-d', '--debug',
        help='Log as much information as possible',
        action='store_true')

    group.add_argument(
        '-q', '--quiet',
        help='Silent mode, log only warnings and errors',
        action='store_true')

    parser.add_argument(
        '-v', '--version',
        help='Print version of this software',
        action='version',
        version='%(prog)s ' + __version__)

    args = parser.parse_args(args)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        log.setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
        log.setLevel(logging.WARNING)
    else:
        logging.getLogger().setLevel(logging.INFO)
        log.setLevel(logging.INFO)

    if 'version' in args:
        print(args.version)

    args.fittings = args.fittings[0]
    log.debug("- loading '{}'".format(args.fittings))

    args.action = args.action[0].lower()

    args.blueprints = []
    args.facilities = []
    for token in args.tokens:
        if token[0] == '@':
            if token == '@':
                raise ValueError("Missing location after @. "
                                 "Correct example: '@AU11'")
            args.facilities.append(token[1:])
        else:
            args.blueprints.append(token)

    if len(args.blueprints) < 1:
        args.blueprints = None
    else:
        log.debug('blueprints: '+' '.join(args.blueprints))

    if len(args.facilities) < 1:
        args.facilities = None
    else:
        log.debug('facilities: '+' '.join(args.facilities))

    return args


def main(args=None, engine=None):
    """
    Runs plumbery from the command line

    :param args: arguments to be considered for this invocation
    :type args: a list of ``str``

    :param engine: an instance of the plumbery engine
    :type engine: :class:`plumbery.PlumberEngine`

    Example::

        $ python -m plumbery fittings.yaml build web

    In this example, plumbery loads fittings plan from ``fittings.yaml``, then
    it builds the blueprint named ``web``.

    If no blueprint is mentioned, then plumbery looks at all blueprint
    definitions in the fittings plan. In other terms, the following command
    builds the entire fittings plan, eventually across multiple facilities::

        $ python -m plumbery fittings.yaml build

    Of course, plumbery can be invoked through the entire life cycle of your
    fittings::

        $ python -m plumbery fittings.yaml build
        $ python -m plumbery fittings.yaml start
        $ python -m plumbery fittings.yaml polish

        ... nodes are up and running ...

        $ python -m plumbery fittings.yaml stop

        ... nodes have been stopped ...

        $ python -m plumbery fittings.yaml wipe

        ... nodes have been destroyed, but the infrastructure remains ...

        $ python -m plumbery fittings.yaml destroy

        ... every virtual resources has been removed ...


    To focus at a single location, put the character '@' followed by the id.
    For example, to build fittings only at 'NA12' you would type::

        $ python -m plumbery fittings.yaml build @NA12

    To focus on one blueprint just mention its name on the command line.
    For example, if fittings plan has a blueprint for nodes running Docker,
    then you may use following statements to bootstrap each node::

        $ python -m plumbery fittings.yaml build docker
        $ python -m plumbery fittings.yaml start docker
        $ python -m plumbery fittings.yaml prepare docker

        ... Docker is up and running at multiple nodes ...

    If you create a new polisher and put it in the directory
    ``plumbery\polishers``, then it will become automatically available::

        $ python -m plumbery fittings.yaml my_special_stuff

    To get some help, you can type::

        $ python -m plumbery -h

    """

    # part 1 - understand what the user wants

    if args is None:
        args = sys.argv[1:]

    try:
        args = parse_args(args)

    except Exception as feedback:
        logging.error("Incorrect arguments. "
                      "Maybe the following can help: python -m plumbery -h")
        if log.getEffectiveLevel() == logging.DEBUG:
            raise
        else:
            log.error("{}: {}".format(
                feedback.__class__.__name__,
                str(feedback)))
        sys.exit(2)

    # part 2 - get a valid and configured engine

    if engine is None:
        try:
            engine = PlumberyEngine(args.fittings, args.parameters)

            if args.safe:
                engine.safeMode = True

        except Exception as feedback:
            if log.getEffectiveLevel() == logging.DEBUG:
                log.error("Cannot read fittings plan from '{}'".format(
                    args.fittings))
                raise
            else:
                log.error("Cannot read fittings plan from '{}'"
                              ", run with -d for debug".format(
                                  args.fittings))
                log.error("{}: {}".format(
                    feedback.__class__.__name__,
                    str(feedback)))
            sys.exit(2)

    # part 3 - do the job

    try:
        engine.do(args.action, args.blueprints, args.facilities)

        log.info(engine.document_elapsed())

    except Exception as feedback:
        if log.getEffectiveLevel() == logging.DEBUG:
            log.error("Unable to do '{}'".format(args.action))
            raise
        else:
            log.error("Unable to do '{}', run with -d for debug".format(
                args.action))
            log.error("{}: {}".format(
                feedback.__class__.__name__,
                str(feedback)))
        sys.exit(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Aborted by user")
        sys.exit(0)
