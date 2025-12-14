package com.language_proximity_analysis.model;

import java.util.HashMap;
import java.util.Map;

public class TableEntry {
    private String name;
    private Map<String, Double> values;
    public TableEntry(String topic){
        this.name = topic;
        values = new HashMap<>();
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public Map<String, Double> getValues() {
        return values;
    }
    public void setValues(Map<String, Double> proximity) {
        this.values = proximity;
    }
    public double getValue(String lang){
        return values.get(lang);
    }
    public void addProximity(String language, double proximity){
        this.values.put(language, proximity);
    }
}
