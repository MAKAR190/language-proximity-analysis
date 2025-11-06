package com.language_proximity_analysis.controller;

import org.graphstream.graph.Graph;
import org.graphstream.ui.fx_viewer.FxViewPanel;
import org.graphstream.ui.fx_viewer.FxViewer;

import com.language_proximity_analysis.graphstream.GraphManager;

import javafx.fxml.FXML;
import javafx.scene.layout.StackPane;

public class GraphViewController {
    @FXML
    private StackPane graphView;

    private Graph graph;
    private FxViewer viewer;
    private FxViewPanel viewPanel;
    private GraphManager graphManager = GraphManager.getInstance();

    @FXML
    public void initialize() {

    }

    public void updateGraph(String word, int depth) {
        if (viewer != null) {
            viewer.close();
            graphView.getChildren().clear();
        }
        word = word.toLowerCase();
        graph = graphManager.findGraph(word, depth);
        graph.setAttribute("ui.stylesheet", "url('src\\main\\resources\\css\\graph.css')");
        viewer = new FxViewer(graph, FxViewer.ThreadingModel.GRAPH_IN_ANOTHER_THREAD);
        viewer.enableAutoLayout();

        viewPanel = (FxViewPanel) viewer.addDefaultView(false);
        graphView.getChildren().add(viewPanel);
    }

    public Graph getGraph() {
        return graph;
    }
}
