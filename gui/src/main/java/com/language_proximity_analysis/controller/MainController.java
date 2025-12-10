package com.language_proximity_analysis.controller;

import javafx.fxml.FXML;
import javafx.scene.control.SplitPane;
import javafx.scene.layout.AnchorPane;

public class MainController {

    @FXML
    private MenuBarController menuBarController;
    @FXML
    private GraphSidebarController graphSidebarController;
    @FXML
    private GraphViewController graphViewController;
    @FXML
    private AnalysisViewController analysisViewController;
    @FXML
    private SplitPane splitPane;

    @FXML
    public void initialize() {
        menuBarController.setMainController(this);
        graphSidebarController.setOnSelectionChanged((word, depth) -> graphViewController.updateGraph(word, depth));
        showGraphView();
    }

    public void showGraphView() {
        graphViewController.getRoot().setVisible(true);
        graphViewController.getRoot().setManaged(true);

        analysisViewController.getRoot().setVisible(false);
        analysisViewController.getRoot().setManaged(false);
    }

    public void showAnalysisView() {
        analysisViewController.getRoot().setVisible(true);
        analysisViewController.getRoot().setManaged(true);
        analysisViewController.updateInfo("en");

        graphViewController.getRoot().setVisible(false);
        graphViewController.getRoot().setManaged(false);
    }
}