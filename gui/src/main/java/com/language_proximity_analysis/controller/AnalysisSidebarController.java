package com.language_proximity_analysis.controller;

import java.util.ArrayList;
import java.util.function.BiConsumer;

import com.language_proximity_analysis.graphstream.GraphManager;
import com.language_proximity_analysis.utils.TextFormatter;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.ListView;
import javafx.scene.control.Slider;
import javafx.scene.layout.VBox;
import javafx.util.StringConverter;

public class AnalysisSidebarController {
    @FXML
    private VBox analysisSidebar;
    @FXML
    private Slider analysisDepthSlider;
    @FXML
    private ChoiceBox<String> languageChoiceBox;
    @FXML
    private ListView<String> optionsList;

    private GraphManager graphManager = GraphManager.getInstance();

    private BiConsumer<String, String> onSelectionChanged;

    public VBox getRoot() {
        return analysisSidebar;
    }

    public void setOnSelectionChanged(BiConsumer<String, String> callback) {
        this.onSelectionChanged = callback;
    }

    @FXML
    public void initialize() {
        languageChoiceBox.getItems().addAll("en", "es", "fr", "pl");
        languageChoiceBox.setValue("en");
        languageChoiceBox.getSelectionModel().selectedItemProperty()
                .addListener((observable, oldValue, newValue) -> triggerUpdate());
        analysisDepthSlider.setLabelFormatter(new StringConverter<Double>() {
            @Override
            public String toString(Double n) {
                if (n < 2)
                    return "Word";
                return "Topic";
            }

            @Override
            public Double fromString(String s) {
                switch (s) {
                    case "Word":
                        return 1d;
                    case "Topic":
                        return 2d;
                    default:
                        return 2d;
                }
            }
        });
        analysisDepthSlider.setValue(2);
        ObservableList<String> observableOptions = FXCollections.observableArrayList();
        optionsList.setItems(observableOptions);

        analysisDepthSlider.valueProperty().addListener((obs, oldVal, newVal) -> {
            updateOptionsList(observableOptions);
        });
        optionsList.getSelectionModel().selectedItemProperty().addListener((obs, oldVal, newVal) -> triggerUpdate());
        updateOptionsList(observableOptions);
    }

    private void triggerUpdate() {
        if (onSelectionChanged != null) {
            String word = optionsList.getSelectionModel().getSelectedItem();
            onSelectionChanged.accept(languageChoiceBox.getValue(), word);
        }
    }

    private void updateOptionsList(ObservableList<String> observableOptions) {
        observableOptions.clear();

        int depth = (int) analysisDepthSlider.getValue();
        ArrayList<String> topics;
        if (depth == 1) {
            topics = graphManager.getTopics();
            for (String topic : topics) {
                observableOptions.add(TextFormatter.capitalizeFirstLetter(topic));
            }
        }
    }
}
