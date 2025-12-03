package com.language_proximity_analysis.controller;

import java.util.List;
import java.util.function.BiConsumer;

import org.graphstream.graph.Graph;

import com.language_proximity_analysis.graphstream.GraphManager;
import com.language_proximity_analysis.utils.TextFormatter;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.fxml.FXML;
import javafx.scene.control.ListView;
import javafx.scene.control.Slider;
import javafx.scene.control.TextField;
import javafx.util.StringConverter;

public class SidebarController {

    @FXML
    private Slider depthSlider;
    @FXML
    private TextField searchField;
    @FXML
    private ListView<String> graphList;
    private GraphManager graphManager = GraphManager.getInstance();

    private BiConsumer<String, Integer> onSelectionChanged;

    public void setOnSelectionChanged(BiConsumer<String, Integer> callback) {
        this.onSelectionChanged = callback;
    }

    @FXML
    public void initialize() {
        depthSlider.setLabelFormatter(new StringConverter<Double>() {
            @Override
            public String toString(Double n) {
                if (n < 2)
                    return "Word";
                if (n < 3)
                    return "Topic";
                return "Language";
            }

            @Override
            public Double fromString(String s) {
                switch (s) {
                    case "Word":
                        return 1d;
                    case "Topic":
                        return 2d;
                    case "Language":
                        return 3d;
                    default:
                        return 3d;
                }
            }
        });

        ObservableList<String> observableOptions = FXCollections.observableArrayList();
        FilteredList<String> filteredOptions = new FilteredList<>(observableOptions, s -> true);
        graphList.setItems(filteredOptions);

        // Filter when typing in search box
        searchField.textProperty().addListener((obs, oldValue, newValue) -> {
            String filter = newValue.toLowerCase();
            filteredOptions.setPredicate(word -> filter.isEmpty() || word.toLowerCase().contains(filter));
        });

        depthSlider.valueProperty().addListener((obs, oldVal, newVal) -> {
            updateGraphList(observableOptions);
            triggerUpdate();
        });

        graphList.getSelectionModel().selectedItemProperty().addListener((obs, oldVal, newVal) -> triggerUpdate());
        updateGraphList(observableOptions);
    }

    private void triggerUpdate() {
        if (onSelectionChanged != null) {
            String word = graphList.getSelectionModel().getSelectedItem();
            if (word != null){
                onSelectionChanged.accept(word, (int) depthSlider.getValue());
            }
        }
    }

    private void updateGraphList(ObservableList<String> observableOptions) {
        observableOptions.clear();

        int depth = (int) depthSlider.getValue();
        List<Graph> graphs;

        switch (depth) {
            case 1:
                graphs = graphManager.getWordGraphs();
                break;
            case 2:
                graphs = graphManager.getTopicGraphs();
                break;
            case 3:
            default:
                graphs = graphManager.getLanguageGraphs();
                break;
        }

        for (Graph graph : graphs) {
            observableOptions.add(TextFormatter.capitalizeFirstLetter(graph.getId()));
        }
    }
}