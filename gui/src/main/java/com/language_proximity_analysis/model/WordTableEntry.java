package com.language_proximity_analysis.model;

import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class WordTableEntry {
    private final StringProperty word = new SimpleStringProperty();

    public StringProperty wordProperty() { return word; }
}
