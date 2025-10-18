package com.language_proximity_analysis.graphstream;

import java.io.FileReader;
import java.util.ArrayList;
import java.util.Map;

import org.graphstream.graph.Edge;
import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.implementations.SingleGraph;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class DataLoader {
    public static ArrayList<Graph> load(String filename) throws Exception{
        JsonObject root = JsonParser.parseReader(new FileReader(filename)).getAsJsonObject();
        ArrayList<Graph> graphs = new ArrayList<>();
        for(Map.Entry<String, JsonElement> entry: root.entrySet()){
            String base = entry.getKey();
            JsonObject graphData = entry.getValue().getAsJsonObject();
            Graph graph = new SingleGraph(base);

            for (JsonElement nodeEl : graphData.getAsJsonArray("nodes")) {
                JsonObject nodeData = nodeEl.getAsJsonObject();
                String id = nodeData.get("id").getAsString();
                Node node = graph.addNode(id);
                for (Map.Entry<String, JsonElement> attr : nodeData.entrySet()) {
                    if (!attr.getKey().equals("id")) {
                        node.setAttribute(attr.getKey(), attr.getValue().getAsString());
                    }
                }
            }

            for (JsonElement edgeEl : graphData.getAsJsonArray("edges")) {
                JsonObject edgeData = edgeEl.getAsJsonObject();
                String source = edgeData.get("source").getAsString();
                String target = edgeData.get("target").getAsString();
                String edgeId = source + "_" + target;
                Edge edge = graph.addEdge(edgeId, source, target, false); // undirected
                if (edgeData.has("weight")) {
                    edge.setAttribute("weight", edgeData.get("weight").getAsDouble());
                }
            }

            graphs.add(graph);
        }
        return graphs;
    }
}
