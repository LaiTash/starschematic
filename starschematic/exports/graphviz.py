import graphviz as gv
from starschematic import visit, value
from random import choice, seed

__author__ = 'Lai Tash'


class GraphBuilder(visit.Visitor):
    arrow_colors = [
        'black', 'green', 'red', '#770099', 'blue', 'magenta',
        '#77aa00', '#007799', 'darkgreen'
    ]

    styles = {
        'Node': {
            'shape': 'box',
        },
        'SwitchXOR': {
            'shape': 'hexagon',
        },
        'SwitchOR': {
            'shape': 'triangle',
        },
        'SwitchAND': {
            'shape': 'invtriangle',
        },
        'AND': {
            'shape': 'invtriangle',
        },
        'SwitchNOT': {
            'shape': 'doubleoctagon',
        },
        'NOT': {
            'shape': 'doubleoctagon',
        },

        'Compound': {
            'color': 'black',
        },

        'Button': {
            'shape': 'circle',
        },
        'PersistentSwitch': {
            'shape': 'signature',
        },
        'Informer': {
            'shape': 'Mcircle',
        },
        'Switch': {
            'shape': 'component'
        },
        'Timer': {
            'shape': 'doublecircle',
        },
        'Transmitter': {
            'shape': 'rarrow',
            'color': 'blue',
        }
    }

    def __init__(self):
        self.cluster_count = 0
        self.styles = self.styles

    def pick_style(self, node):
        for cls in node.__class__.mro():
            style = self.styles.get(cls.__name__)
            if style is not None:
                return style
        return {}

    def visit_Node(self, node, graph):
        style = self.pick_style(node).copy()
        style['color'] = 'green' if value(node) else style.get('color')
        graph.node(node.uuid, label=node.name,
                   style='filled',
                   **style)
        for input in node.inputs:
            for signal in input.inputs:
                label = input._name
                if label == 'input':
                    label = None
                seed(hash(label))
                self.root_graph.edge(signal.node.uuid, node.uuid, label=label,
                                     color=choice(self.arrow_colors))


    def visit_Compound(self, node, graph=None):
        parent = graph
        graph = gv.Digraph(name='cluster_%i' % self.cluster_count,format='png')
        if not parent:
            self.root_graph = graph
        self.cluster_count += 1
        graph.graph_attr.update(self.pick_style(node))
        graph.graph_attr.update({'label': node.name})
        #graph.graph_attr.update({'bgcolor': '#%i33333' % random.randint(0, 99)})
        for child in node.children.values():
            self.visit(child, graph)
        if parent:
            parent.subgraph(graph)
        return graph