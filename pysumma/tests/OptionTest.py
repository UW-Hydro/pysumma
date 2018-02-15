from pysumma.Decision import *
#from pysumma.ProposedDecisions import *
from pysumma.ProposedDecisions import PDecisionOption
from pysumma.Simulation import *
from pysumma.Option import *

# The old way of doing things, with different option classes
Decision_Option = DecisionOption("soilCatTbl", "tmp_Decision.txt")
File_Option = FileManagerOption("meta_time", "tmp_fileManager.txt")

PDecision_Option = PDecisionOption("soilCatTbl", "tmp_Decision.txt")

assert(Decision_Option.line_contents == PDecision_Option.line_contents)
assert(Decision_Option.line_no == PDecision_Option.line_no)
assert(Decision_Option.get_default_value() == PDecision_Option.get_value(1))

