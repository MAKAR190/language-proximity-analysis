package com.language_proximity_analysis.graphstream;

import java.util.ArrayList;

import org.graphstream.graph.Graph;

import com.google.gson.JsonObject;

public class GraphManager {
    private static GraphManager instance;
    private ArrayList<Graph> wordGraphs;
    private ArrayList<Graph> topicGraphs;
    private ArrayList<Graph> languageGraphs;

    private GraphManager() {
        try {
            JsonObject wordJson = DataLoader.load("data/analysis/word_distance.json");
            JsonObject topicJson = DataLoader.load("data/analysis/topic_proximity.json");
            JsonObject languageJson = DataLoader.load("data/analysis/global_proximity.json");

            wordGraphs = GraphBuilder.buildGraphsFromJson(wordJson);
            topicGraphs = GraphBuilder.buildGraphsFromJson(topicJson);
            languageGraphs = GraphBuilder.buildGraphsFromJson(languageJson);
        } catch (Exception e) {
            System.err.println(e);
        }
    }

    public static GraphManager getInstance(){
        if(instance == null){
            instance = new GraphManager();
        }
        return instance;
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

    public Graph findGraph(String word, int depth){
        ArrayList<Graph> currentDepthGraphs = new ArrayList<>();
        switch (depth) {
            case 1:
                currentDepthGraphs = wordGraphs;
                break;
            case 2:
                currentDepthGraphs = topicGraphs;
                break;
            case 3:
                currentDepthGraphs = languageGraphs;
                break;
        }
        for(Graph graph : currentDepthGraphs){
            if(graph.getId().equals(word)){
                return graph;
            }
        }
        return null;
    }
}
