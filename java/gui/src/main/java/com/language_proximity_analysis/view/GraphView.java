package com.language_proximity_analysis.view;

import org.graphstream.graph.Graph;
import org.graphstream.graph.implementations.SingleGraph;
import org.graphstream.ui.fx_viewer.FxViewPanel;
import org.graphstream.ui.fx_viewer.FxViewer;

import javafx.scene.layout.StackPane;

public class GraphView extends StackPane{
    private Graph graph;
     public GraphView() {
        graph = new SingleGraph("MyGraph");

        graph.addNode("A");
        graph.addNode("B");
        graph.addEdge("AB", "A", "B");

        FxViewer viewer = new FxViewer(graph, FxViewer.ThreadingModel.GRAPH_IN_ANOTHER_THREAD);
        viewer.enableAutoLayout();
        FxViewPanel viewPanel = (FxViewPanel) viewer.addDefaultView(false);
        this.getChildren().add(viewPanel);
    }

    public Graph getGraph() {
        return graph;
    }
}
