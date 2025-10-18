package com.language_proximity_analysis.view;

import org.graphstream.graph.Graph;
import org.graphstream.graph.implementations.SingleGraph;
import org.graphstream.ui.fx_viewer.FxViewPanel;
import org.graphstream.ui.fx_viewer.FxViewer;

import com.language_proximity_analysis.graphstream.GraphManager;

import javafx.scene.layout.StackPane;

public class GraphView extends StackPane{
    private Graph graph;
     public GraphView() {
        GraphManager graphManager = new GraphManager();
        graph = graphManager.getWordGraphs().get(0);

        FxViewer viewer = new FxViewer(graph, FxViewer.ThreadingModel.GRAPH_IN_ANOTHER_THREAD);
        viewer.enableAutoLayout();
        FxViewPanel viewPanel = (FxViewPanel) viewer.addDefaultView(false);
        this.getChildren().add(viewPanel);
    }

    public Graph getGraph() {
        return graph;
    }
}
