import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.utils import get_example_model

def generate_example_model():
    paper_model = BayesianNetwork(
        [
            ("A","B"),
            ("A","C"),
        ]
    )
    cpd_a = TabularCPD(
        variable="A", variable_card=2, values=[[0.1], [0.9]]
    )
    cpd_b = TabularCPD(
        variable="B", variable_card=2, values=[[0.1, 0.2], [0.9, 0.8]], evidence=["A"], evidence_card=[2]
    )
    cpd_c = TabularCPD(
        variable="C", variable_card=3, values=[[0.1, 0.01], [0.2, 0.09], [0.7, 0.9]], evidence=["A"], evidence_card=[2]
    ) 
    paper_model.add_cpds(
        cpd_a,cpd_b,cpd_c
    )
    assert paper_model.check_model() # Sanity check
    return paper_model

def generate_alarm_model():
    alarm_model = BayesianNetwork(
        [
            ("Burglary", "Alarm"),
            ("Earthquake", "Alarm"),
            ("Alarm", "JohnCalls"),
            ("Alarm", "MaryCalls"),
        ]
    )
    cpd_burglary = TabularCPD(
    variable="Burglary", variable_card=2, values=[[0.999], [0.001]]
    )
    cpd_earthquake = TabularCPD(
        variable="Earthquake", variable_card=2, values=[[0.998], [0.002]]
    )
    cpd_alarm = TabularCPD(
        variable="Alarm",
        variable_card=2,
        values=[[0.999, 0.71, 0.06, 0.05], [0.001, 0.29, 0.94, 0.95]],
        evidence=["Burglary", "Earthquake"],
        evidence_card=[2, 2],
    )
    cpd_johncalls = TabularCPD(
        variable="JohnCalls",
        variable_card=2,
        values=[[0.95, 0.1], [0.05, 0.9]],
        evidence=["Alarm"],
        evidence_card=[2],
    )
    cpd_marycalls = TabularCPD(
        variable="MaryCalls",
        variable_card=2,
        values=[[0.1, 0.7], [0.9, 0.3]],
        evidence=["Alarm"],
        evidence_card=[2],
    )

    # Associating the parameters with the model structure
    alarm_model.add_cpds(
        cpd_burglary, cpd_earthquake, cpd_alarm, cpd_johncalls, cpd_marycalls
    )
    assert alarm_model.check_model() # Sanity check
    return alarm_model

def generate_asia_model():
    asia = get_example_model('asia')
    assert asia.check_model() # Sanity check
    return asia

def generate_cancer_model():
    cancer = get_example_model('cancer')
    assert cancer.check_model() # Sanity check
    return cancer

def display_network(model):
    pos = nx.circular_layout(model)
    nx.draw(model, pos=pos, with_labels=True)
    plt.show()

if __name__ == "__main__":
    model = generate_asia_model()
    print(model)
    print(f"Model has CPDs: {model.get_cpds()}")
    print(f"Model has nodes: {model.nodes()}")
    print(f"Model has edges: {model.edges()}")
    # Listing all Independencies
    # print(f"Independence in the model:\n{model.get_independencies()}")
    display_network(model)