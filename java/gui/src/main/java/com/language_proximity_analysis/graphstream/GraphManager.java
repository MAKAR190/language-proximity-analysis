package com.language_proximity_analysis.graphstream;

import java.util.ArrayList;

import org.graphstream.graph.Graph;

public class GraphManager {
    private ArrayList<Graph> wordGraphs;
    private ArrayList<Graph> topicGraphs;
    private ArrayList<Graph> languageGraphs;

    public GraphManager() {
        try {
            wordGraphs = DataLoader.load("src\\main\\resources\\data\\words.json");
        } catch (Exception e) {
            System.err.println(e);
        }
    }

    public ArrayList<Graph> getWordGraphs() {
        return wordGraphs;
    }

    public ArrayList<Graph> getTopicGraphs() {
        return topicGraphs;
    }

    public ArrayList<Graph> getLanguageGraphs() {
        return languageGraphs;
    }
}
