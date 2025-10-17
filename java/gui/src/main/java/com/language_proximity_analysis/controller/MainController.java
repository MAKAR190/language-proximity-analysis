package com.language_proximity_analysis.controller;

import javafx.fxml.FXML;

public class MainController {

    @FXML private MenuBarController menuBarPaneController;
    @FXML private SidebarController sidebarPaneController;
    // @FXML private GraphViewController graphPaneController;

    @FXML
    public void initialize() {
        // Example of connecting subcontrollers:
        // sidebarPaneController.setOnSelectionChanged((word, depth) ->
        //         graphPaneController.updateGraph(word, depth)
        // );
    }
}