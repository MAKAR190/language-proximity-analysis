package com.language_proximity_analysis.controller;

import javafx.fxml.FXML;

public class MainController {

    @FXML private MenuBarController menuBarController;
    @FXML private SidebarController sidebarController;
    @FXML private GraphViewController graphViewController;

    @FXML
    public void initialize() {
        sidebarController.setOnSelectionChanged((word, depth) ->
                graphViewController.updateGraph(word, depth)
        );
    }
}