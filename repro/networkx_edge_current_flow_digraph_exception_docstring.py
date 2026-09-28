"""networkx edge_current_flow_betweenness_centrality: a directed graph raises NetworkXNotImplemented, but the docstring says NetworkXError.

The Raises section documents NetworkXError for directed graphs ('The algorithm does not
support DiGraphs'). The function raises NetworkXNotImplemented, which is not a subclass
of NetworkXError, so code that catches the documented exception does not catch it. The
script reads the installed docstring.

Run: python networkx_edge_current_flow_digraph_exception_docstring.py
Exit status: 1 = the discrepancy was detected in the installed version; 0 = not reproduced by
this comparison; 2 = the script could not run or a precondition failed.
"""
import os
import sys
import traceback


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)


def _could_not_run(exc_type, exc, tb):
    traceback.print_exception(exc_type, exc, tb)
    print(f"could not run: {exc_type.__name__}: {exc}")
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(2)


sys.excepthook = _could_not_run

import inspect
import networkx as nx

doc = " ".join(inspect.getdoc(nx.edge_current_flow_betweenness_centrality).split())
documented = "NetworkXError The algorithm does not support DiGraphs" in doc
subclass = issubclass(nx.NetworkXNotImplemented, nx.NetworkXError)
try:
    nx.edge_current_flow_betweenness_centrality(nx.DiGraph([(0, 1), (1, 2)]))
    verdict(False, "no exception raised")
except nx.NetworkXNotImplemented as e:
    verdict(documented and not subclass, f"raised NetworkXNotImplemented ({e}); subclass of NetworkXError: {subclass}; "
                                         f"docstring documents NetworkXError for DiGraphs: {documented}")
except nx.NetworkXError as e:
    verdict(False, f"raised the documented NetworkXError: {e}")
