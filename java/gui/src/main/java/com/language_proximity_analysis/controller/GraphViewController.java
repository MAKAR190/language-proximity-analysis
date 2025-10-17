package com.language_proximity_analysis.controller;

import com.language_proximity_analysis.view.GraphView;

import javafx.fxml.FXML;

public class GraphViewController {
    @FXML
    private GraphView graphView;

    @FXML
    public void initialize() {
        graphView.getGraph().addNode("C");
        graphView.getGraph().addEdge("BC", "B", "C");
        graphView.getGraph().addEdge("AC", "A", "C");
    }
}
