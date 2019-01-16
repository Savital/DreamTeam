import os

from app import create_app
#from pycallgraph import PyCallGraph
#from pycallgraph.output import GraphvizOutput

config_name = os.getenv('FLASK_CONFIG')

#graphviz = GraphvizOutput()
#graphviz.output_file = 'basic.png'

#with PyCallGraph(output=graphviz):
app = create_app(config_name)

if __name__ == '__main__':
    app.run()

