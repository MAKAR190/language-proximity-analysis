package com.language_proximity_analysis.controller;

import javafx.fxml.FXML;
import javafx.scene.control.SplitPane;

public class MainController {

    @FXML
    private MenuBarController menuBarController;
    @FXML
    private GraphSidebarController graphSidebarController;
    @FXML
    private GraphViewController graphViewController;
    @FXML
    private AnalysisSidebarController analysisSidebarController;
    @FXML
    private AnalysisViewController analysisViewController;
    @FXML
    private SplitPane splitPane;

    @FXML
    public void initialize() {
        menuBarController.setMainController(this);
        graphSidebarController.setOnSelectionChanged((word, depth) -> graphViewController.updateGraph(word, depth));
        showGraphView();
        //analysisSidebarController.setOnMainLanguageChanged((lang) -> analysisViewController.updateTable(lang, "vegetables"));
        analysisSidebarController.setOnSelectionChanged((lang, topic) -> analysisViewController.updateTable(lang, topic));
    }

    public void showGraphView() {
        graphViewController.getRoot().setVisible(true);
        graphViewController.getRoot().setManaged(true);
        graphSidebarController.getRoot().setVisible(true);
        graphSidebarController.getRoot().setManaged(true);

        analysisViewController.getRoot().setVisible(false);
        analysisViewController.getRoot().setManaged(false);
        analysisSidebarController.getRoot().setVisible(false);
        analysisSidebarController.getRoot().setManaged(false);
    }

    public void showAnalysisView() {
        analysisViewController.getRoot().setVisible(true);
        analysisViewController.getRoot().setManaged(true);
        analysisSidebarController.getRoot().setVisible(true);
        analysisSidebarController.getRoot().setManaged(true);

        graphViewController.getRoot().setVisible(false);
        graphViewController.getRoot().setManaged(false);
        graphSidebarController.getRoot().setVisible(false);
        graphSidebarController.getRoot().setManaged(false);
    }
}