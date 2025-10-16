package com.language_proximity_analysis.controller;

import java.util.function.BiConsumer;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.fxml.FXML;
import javafx.scene.control.ListView;
import javafx.scene.control.Slider;
import javafx.scene.control.TextField;
import javafx.util.StringConverter;

public class SidebarController {

    @FXML private Slider depthSlider;
    @FXML private TextField searchField;
    @FXML private ListView<String> graphList;

    private BiConsumer<String, Integer> onSelectionChanged;
    private final ObservableList<String> allOptions = FXCollections.observableArrayList("Alpha", "Beta", "Gamma", "Delta", "Epsilon");

    public void setOnSelectionChanged(BiConsumer<String, Integer> callback) {
        this.onSelectionChanged = callback;
    }

    @FXML
    public void initialize() {
        depthSlider.setLabelFormatter(new StringConverter<Double>() {
            @Override
            public String toString(Double n) {
                if (n < 2) return "Word";
                if (n < 3) return "Topic";
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
        FilteredList<String> filteredOptions = new FilteredList<>(allOptions, s -> true);
        graphList.setItems(filteredOptions);

        // Filter when typing in search box
        searchField.textProperty().addListener((obs, oldValue, newValue) -> {
            String filter = newValue.toLowerCase();
            filteredOptions.setPredicate(word ->
                filter.isEmpty() || word.toLowerCase().contains(filter)
            );
        });
        
        graphList.getSelectionModel().selectedItemProperty().addListener((obs, oldVal, newVal) -> triggerUpdate());
        depthSlider.valueProperty().addListener((obs, oldVal, newVal) -> triggerUpdate());
    }

    private void triggerUpdate() {
        if (onSelectionChanged != null) {
            String word = graphList.getSelectionModel().getSelectedItem();
            if (word != null)
                onSelectionChanged.accept(word, (int) depthSlider.getValue());
        }
    }
}