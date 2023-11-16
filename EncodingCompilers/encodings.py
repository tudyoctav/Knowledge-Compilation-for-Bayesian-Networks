from pgmpy.models import BayesianModel
from sympy import symbols, Not, Equivalent, Implies
from sympy.logic.boolalg import Or, And, to_cnf
import itertools
from EncodingCompilers.dimacs import to_dimacs_formula


def generate_ENC1_encoding(bayesian_model : BayesianModel):

    indicator_clauses = []
    # Dictionary that maps each node and state to an indicator variable (e.g. λ_A_0 for node A and state 0)
    symb_dict_indicator = {node: {state: symbols(f"λ_{node}_{state}") for state in bayesian_model.get_cpds(node).state_names[node]} for node in bayesian_model.nodes()}
    print(symb_dict_indicator)
    # Add indicator clauses
    for node in bayesian_model.nodes():
        clause = []
        print(f"Node: {node} has cardinality: {bayesian_model.get_cardinality(node)}")
        node_states = bayesian_model.get_cpds(node).state_names[node]
        # Add the clause that at least one state must be true
        for state in node_states:
            clause.append(symb_dict_indicator[node][state])
        indicator_clauses.append(clause)
        # Add the clause that at most one state can be true
        for i in range(len(node_states)):
            for j in range(i+1, len(node_states)):
                indicator_clauses.append([Not(symb_dict_indicator[node][node_states[i]]), Not(symb_dict_indicator[node][node_states[j]])])

    # Dictionary that maps each node without evidence and state to a parameter variable (e.g. Θ_A_0 for node A and state 0)
    symb_dict_param_no_evidence = {node: {state: symbols(f"Θ_{node}_{state}") for state in bayesian_model.get_cpds(node).state_names[node]} for node in bayesian_model.nodes()}
    print(symb_dict_param_no_evidence)
    # Dictionary that maps each node, state and evidence state to a parameter variable (e.g. Θ_A_0|B_1;C_2 for node A and state 0 and evidence node B and C with evidence state 1 and 2 respectively)
    symb_dict_param_with_evidence = {node: {state :{evidence_state: symbols(f"Θ_{node}_{state}|{(';'.join([(str(bayesian_model.get_cpds(node).get_evidence()[i]) +'_'+ str(el)) for i,el in enumerate(evidence_state)])).replace(' ','')}") for evidence_state in itertools.product(*[bayesian_model.get_cpds(node).state_names[evidence_node] for evidence_node in bayesian_model.get_cpds(node).get_evidence()])} for state in bayesian_model.get_cpds(node).state_names[node]} for node in bayesian_model.nodes()}
    # Note that we could combine the two dictionaries above using an if statement (or just used (,) as the third key for nodes without evidence), but this would make the code even more unreadable
    print(symb_dict_param_with_evidence)
    # Initialize parameter clauses
    param_clauses = []
    # Add parameter clauses
    for node in bayesian_model.nodes():
        node_states = bayesian_model.get_cpds(node).state_names[node]
        evidence = bayesian_model.get_cpds(node).get_evidence()
        evidence_states = [bayesian_model.get_cpds(node).state_names[evidence_node] for evidence_node in evidence]
        print(f"Node {node} has states: {node_states}")
        print(f"Node {node} has evidence: {evidence}")
        print(f"Node {node} has evidence states: {evidence_states}")
        if len(evidence) == 0: #if there is no evidence, we just need to ensure consistency between the indicator and parameter variables
            print("yay")
            for state in node_states:
                param_clauses.append(Equivalent(symb_dict_indicator[node][state],symb_dict_param_no_evidence[node][state]))
        else: # in case of evidence, the logic is a bit messy
            print(f"Node {node} has cartesian product of evidence states: {list(itertools.product(*evidence_states))}")
            for state in node_states: # for each state of the node
                for evidence_state in itertools.product(*evidence_states): # for each combination of evidence states
                    indicator_params = [symb_dict_indicator[node][state]] # initialize the list of indicator variables
                    for i in range(len(evidence)): # for each evidence variable
                        indicator_params.append(symb_dict_indicator[evidence[i]][evidence_state[i]]) # collect the indicator variables for the current combination of evidence states
                    conjunction = And(*indicator_params) # combine the indicator variables with a conjunction
                    print(Equivalent(conjunction, symb_dict_param_with_evidence[node][state][evidence_state])) # sanity check
                    param_clauses.append(Equivalent(conjunction, symb_dict_param_with_evidence[node][state][evidence_state])) # write the double implication
    # Add clauses together
    # encoding = And(*[Or(*clause) for clause in indicator_clauses])
    # encoding = And(*param_clauses)
    encoding = And(*([Or(*clause) for clause in indicator_clauses] + param_clauses))
    print(f"Resulting encoding: {encoding}")
    # Convert to CNF
    cnf = to_cnf(encoding)
    print(f"Resulting cnf: {cnf}")
    raw_dimacs = generate_dimacs_format(cnf)
    print(f"Resulting raw dimacs:\n{raw_dimacs}")
    dimacs = to_dimacs_formula(cnf)
    print(f"Resulting dimacs:\n{dimacs}")
    return raw_dimacs, dimacs

def generate_ENC2_encoding(bayesian_model : BayesianModel):

    indicator_clauses = []
    # Dictionary that maps each node and state to an indicator variable (e.g. λ_A_0 for node A and state 0)
    symb_dict_indicator = {node: {state: symbols(f"λ_{node}_{state}") for state in bayesian_model.get_cpds(node).state_names[node]} for node in bayesian_model.nodes()}
    print(symb_dict_indicator)
    # Add indicator clauses
    for node in bayesian_model.nodes():
        clause = []
        print(f"Node: {node} has cardinality: {bayesian_model.get_cardinality(node)}")
        node_states = bayesian_model.get_cpds(node).state_names[node]
        # Add the clause that at least one state must be true
        for state in node_states:
            clause.append(symb_dict_indicator[node][state])
        indicator_clauses.append(clause)
        # Add the clause that at most one state can be true
        for i in range(len(node_states)):
            for j in range(i+1, len(node_states)):
                indicator_clauses.append([Not(symb_dict_indicator[node][node_states[i]]), Not(symb_dict_indicator[node][node_states[j]])])

    # Dictionary that maps each node, state and evidence state to a parameter variable (e.g. Θ_A_0|B_1;C_2 for node A and state 0 and evidence node B and C with evidence state 1 and 2 respectively)
    symb_dict_param = {node: {state :{evidence_state: symbols(f"ρ_{node}_{state}|{(';'.join([(str(bayesian_model.get_cpds(node).get_evidence()[i]) +'_'+ str(el)) for i,el in enumerate(evidence_state)])).replace(' ','')}") for evidence_state in itertools.product(*[bayesian_model.get_cpds(node).state_names[evidence_node] for evidence_node in bayesian_model.get_cpds(node).get_evidence()])} for state in bayesian_model.get_cpds(node).state_names[node][:-1]} for node in bayesian_model.nodes()}
    # Note that that we use the empty tuple () as the third key for states without evidence
    print(symb_dict_param)
    # Initialize parameter clauses
    param_clauses = []
    # Add parameter clauses
    for node in bayesian_model.nodes():
        node_states = bayesian_model.get_cpds(node).state_names[node]
        evidence = bayesian_model.get_cpds(node).get_evidence()
        evidence_states = [bayesian_model.get_cpds(node).state_names[evidence_node] for evidence_node in evidence]
        print(f"Node {node} has states: {node_states}")
        print(f"Node {node} has evidence: {evidence}")
        print(f"Node {node} has evidence states: {evidence_states}")
        for index,state in enumerate(node_states): # for each state of the node
            for evidence_state in itertools.product(*evidence_states): # for each combination of evidence states
                indicator_var = [] # initialize the list of indicator variables
                for i in range(len(evidence)): # for each evidence variable
                    indicator_var.append(symb_dict_indicator[evidence[i]][evidence_state[i]]) # collect the indicator variables for the current combination of evidence states
                param_vars = [] # initialize the list of parameter variables
                for i in range(0, index):
                    param_vars.append(Not(symb_dict_param[node][node_states[i]][evidence_state]))
                if state != node_states[-1]: # if the state is not the last one
                    param_vars.append(symb_dict_param[node][state][evidence_state]) # do not negate the curent state
                else:
                    pass # do nothing

                conjunction = And(*(indicator_var + param_vars)) # combine the indicator and parameter variables with a conjunction
                print(Implies(conjunction, symb_dict_indicator[node][state]))
                param_clauses.append(Implies(conjunction, symb_dict_indicator[node][state])) # write the clause
        # Add clauses together
    # encoding = And(*[Or(*clause) for clause in indicator_clauses])
    # encoding = And(*param_clauses)
    encoding = And(*([Or(*clause) for clause in indicator_clauses] + param_clauses))
    print(f"Resulting encoding: {encoding}")
    # Convert to CNF
    cnf = to_cnf(encoding)
    print(f"Resulting cnf: {cnf}")
    raw_dimacs = generate_dimacs_format(cnf)
    print(f"Resulting raw dimacs:\n{raw_dimacs}")
    dimacs = to_dimacs_formula(cnf)
    print(f"Resulting dimacs:\n{dimacs}")
    return raw_dimacs, dimacs

def generate_dimacs_format(cnf):

    # Convert CNF to DIMACS format without replacing variables names with numbers (for debugging purposes)
    dimacs = f"p cnf {len(cnf.args)} {len(cnf.args)}\n"
    for clause in cnf.args:
        dimacs += " ".join(str(literal) for literal in clause.args) + " 0\n"

    return dimacs
