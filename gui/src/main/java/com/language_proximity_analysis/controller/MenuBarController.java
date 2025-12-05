package com.language_proximity_analysis.controller;

import javafx.fxml.FXML;

public class MenuBarController {

    private MainController mainController;

    public void setMainController(MainController mainController) {
        this.mainController = mainController;
    }

    @FXML
    private void onGraphs() {
        mainController.showGraphView();
    }

    @FXML
    private void onAnalysis() {
        mainController.showAnalysisView();
    }
}