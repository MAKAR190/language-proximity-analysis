package com.language_proximity_analysis.controller;

import javafx.fxml.FXML;
import javafx.scene.layout.StackPane;

public class AnalysisViewController {
    // TO DO:
    // heatmap 
    // select topic, select main language
    // rows - words, columns - languages
    // comparison to average value for given language pair
    @FXML private StackPane analysisView;

    public StackPane getRoot() {
        return analysisView;
    }
}
