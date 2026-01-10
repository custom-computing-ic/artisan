#!/usr/bin/env artisan

from artisan import *

import pprint as pp
import sys

class Profiler:
    def __init__(self, cmd=None):
        self.ast = Ast(cmd, parse=False).clone()
        self.data = None

    # returns profiling data
    def run(self, debug=False):
        # finds all outermost for-loops
        results = self.ast.query(select="src{Module} => loop{ForStmt}",
                                 where=lambda loop: loop.is_outermost())

        print("[i] found %d candidate for-loop(s)...!" % len(results))
        if len(results) == 0:
            return 0

        # step 1: include header <artisan> on all matched sources
        srcs = results.apply(RSet.distinct, target='src')
        for res in srcs:
            res.src.instrument(Action.before, code="#include <artisan>\n")

        # step 2: instrument matched loop to add a timer and a iteration counter
        for res in results:
            ltag = res.loop.tag
            res.loop.instrument(Action.before, code='{ artisan::Timer __timer_%s__([](double t) { artisan::Report::write("(0, \'%s\', %%1%%),", t); });'
                            'int __count__%s = 0;' % (ltag, ltag, ltag))
            res.loop.instrument(Action.begin, code= "__count__%s++;" % ltag)
            res.loop.instrument(Action.after, code='artisan::Report::write("(1, \'%s\', %%1%%),", __count__%s);}'
                            % (ltag, ltag))

        # step 3: query main function
        results2 = self.ast.query("fn{FunctionDecl}", where=lambda fn: fn.name == 'main')

        for res in results2:
            res.fn.instrument(Action.begin,
                              code='artisan::Report::connect(); artisan::Report::write("["); int ret;'
                                   '{ artisan::Timer __timer_main__([](double t) { artisan::Report::write("(2, %1%)", t); });'
                                   '  ret = [] (auto argc, auto argv) { ')
            res.fn.instrument(Action.end,
                              code='  }(argc, argv);'
                                   '}'
                                   'artisan::Report::emit("]");'
                                   'artisan::Report::disconnect();'
                                   'return ret;')

        # step 4: sync changes
        self.ast.sync(commit=True)

        # step 5: run
        def report(ast, data):
            self.data = data

        self.ast.exec(report=report)

        if not debug:
            self.ast.discard()

        return len(results)


profiler=Profiler('main.cpp')

n=profiler.run(debug=True)
print("[i] instrumented %d loop(s)." % n)
pp.pprint(profiler.data, indent=3)















