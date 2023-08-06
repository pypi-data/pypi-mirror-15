
import sys

from ..analysis import register_analysis
from .cfg_fast import CFGFast

class OutdatedError(Exception):
    pass

class CFG(CFGFast):
    """
    tl;dr  CFG is just a wrapper around CFGFast for compatibility issues. It will be fully replaced by CFGFast in future
      releases. Feel free to use CFG if you intend to use CFGFast. Please use CFGAccurate if you *have to* use the old,
      slow, but more accurate version of CFG.

    For multiple historical reasons, angr's CFG is accurate but slow, which does not meet what most people expect. We
    developed CFGFast for light-speed CFG recovery, and renamed the old CFG class to CFGAccurate. For compability
    concerns, CFG was kept as an alias to CFGAccurate.

    However, so many new users of angr would load up a binary and generate a CFG immediately after running
    "pip install angr", and draw the conclusion that "angr's CFG is so slow - angr must be unusable!" Therefore, we made
    the hard decision:
                            CFG will be an alias to CFGFast, instead of CFGAccurate.

    To ease the transition of your existing code and script, the following changes are made:
    - A CFG class, which is a sub class of CFGFast, is created.
    - You will see both a warning message printed out to stderr and an exception raised by angr if you are passing CFG
      any parameter that only CFGAccurate supports. This exception is not a sub class of AngrError, so you wouldn't
      capture it with your old code by mistake.
    - In the near future, this wrapper class will be removed completely, and CFG will be a simple alias to CFGFast.

    We expect most interfaces are the same between CFGFast and CFGAccurate. Apparently some functionalities (like
    context-sensitivity, and state keeping) only exist in CFGAccurate, which is when you want to use CFGAccurate
    instead.
    """
    def __init__(self,
                 # parameters that CFGFast takes
                 binary=None,
                 start=None,
                 end=None,
                 pickle_intermediate_results=False,
                 symbols=True,
                 function_prologues=True,
                 resolve_indirect_jumps=True,
                 force_segment=False,
                 force_complete_scan=True,
                 indirect_jump_target_limit=100000,
                 # parameters that only CFGAccurate takes
                 context_sensitivity_level=None,  # pylint: disable=unused-argument
                 avoid_runs=None,  # pylint: disable=unused-argument
                 enable_function_hints=None,  # pylint: disable=unused-argument
                 call_depth=None,  # pylint: disable=unused-argument
                 call_tracing_filter=None,  # pylint: disable=unused-argument
                 initial_state=None,  # pylint: disable=unused-argument
                 starts=None,  # pylint: disable=unused-argument
                 keep_state=None,  # pylint: disable=unused-argument
                 enable_advanced_backward_slicing=None,  # pylint: disable=unused-argument
                 enable_symbolic_back_traversal=None,  # pylint: disable=unused-argument
                 additional_edges=None,  # pylint: disable=unused-argument
                 no_construct=None  # pylint: disable=unused-argument
                 ):


        outdated_exception = "CFG is now an alias to CFGFast."
        outdated_message = "CFG is now an alias to CFGFast. Please switch to CFGAccurate if you need functionalities " \
                           "that only exist there. For most cases, your code should be fine by changing \"CFG(...)\" " \
                           "to \"CFGAccurate(...)\". Sorry for breaking your code with this giant change."

        cfgaccurate_params = {'context_sensitivity_level', 'avoid_runs', 'enable_function_hints', 'call_depth',
                              'call_tracing_filter', 'initial_state', 'starts', 'keep_state',
                              'enable_advanced_backward_slicing', 'enable_symbolic_back_traversal', 'additional_edges',
                              'no_construct'
                              }

        # Sanity check to make sure the user only wants to use CFGFast

        for p in cfgaccurate_params:
            if locals().get(p, None) is not None:
                sys.stderr.write(outdated_message + "\n")
                raise OutdatedError(outdated_exception)

        # Now initializes CFGFast :-)
        CFGFast.__init__(self,
                         binary=binary,
                         start=start,
                         end=end,
                         pickle_intermediate_results=pickle_intermediate_results,
                         symbols=symbols,
                         function_prologues=function_prologues,
                         resolve_indirect_jumps=resolve_indirect_jumps,
                         force_segment=force_segment,
                         force_complete_scan=True,
                         indirect_jump_target_limit=indirect_jump_target_limit
                         )

register_analysis(CFG, 'CFG')
