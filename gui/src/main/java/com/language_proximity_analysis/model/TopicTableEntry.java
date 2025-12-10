package com.language_proximity_analysis.model;

import java.util.HashMap;
import java.util.Map;

public class TopicTableEntry {
    private String topic;
    private Map<String, Double> proximity;
    public TopicTableEntry(String topic){
        this.topic = topic;
        proximity = new HashMap<>();
    }
    public String getTopic() {
        return topic;
    }
    public void setTopic(String topic) {
        this.topic = topic;
    }
    public Map<String, Double> getProximity() {
        return proximity;
    }
    public void setProximity(Map<String, Double> proximity) {
        this.proximity = proximity;
    }
    public void addProximity(String language, double proximity){
        this.proximity.put(language, proximity);
    }
}
