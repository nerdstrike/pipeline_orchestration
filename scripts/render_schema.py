import sqlalchemy
import sqlalchemy_schemadisplay

# graph is a pydot entity. Any render tweaks have to be done that way.
graph = sqlalchemy_schemadisplay.create_schema_graph(
    metadata=sqlalchemy.MetaData('sqlite:///test.db')
    # show_column_keys=True,
)

render_attr = {
    'scale': 2,
    'label': 'Draft orchestration schema',
    'labelloc': 't'
}

for attr, value in render_attr.items():
    graph.set(attr, value)

graph.write_png('test.png', prog='neato')
