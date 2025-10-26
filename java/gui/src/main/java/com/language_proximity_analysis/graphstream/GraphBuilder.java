package com.language_proximity_analysis.graphstream;

import java.util.ArrayList;
import java.util.Map;

import org.graphstream.graph.Edge;
import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.implementations.SingleGraph;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public class GraphBuilder {
    public static ArrayList<Graph> buildGraphsFromJson(JsonObject root) {
        ArrayList<Graph> graphs = new ArrayList<>();
        for (Map.Entry<String, JsonElement> entry : root.entrySet()) {
            String graphId = entry.getKey();
            JsonObject graphData = entry.getValue().getAsJsonObject();
            Graph graph = new SingleGraph(graphId);
            for (JsonElement nodeEl : graphData.getAsJsonArray("nodes")) {
                JsonObject nodeData = nodeEl.getAsJsonObject();

                String id = nodeData.get("id").getAsString();
                Node node = graph.addNode(id);

                String label = TextFormatter.toLabel(id);
                node.setAttribute("ui.label", label);

                String language = nodeData.get("language").getAsString();
                node.setAttribute("ui.class", language);
            }

            for (JsonElement edgeEl : graphData.getAsJsonArray("edges")) {
                JsonObject edgeData = edgeEl.getAsJsonObject();

                String source = edgeData.get("source").getAsString();
                String target = edgeData.get("target").getAsString();
                String edgeId = source + "_" + target;
                Edge edge = graph.addEdge(edgeId, source, target, false); // undirected

                if (edgeData.has("weight")) {
                    edge.setAttribute("ui.label", edgeData.get("weight"));
                    double weight = edgeData.get("weight").getAsDouble();
                    edge.setAttribute("ui.size", weight*10);
                    // layoutWeight is multiplier for edge length
                    // default is 1, larger = longer edge, smaller = shorter edge
                    // our weight works opposite way, so we invert it and remap 0.0-1.0 into 0.5-2.0
                    double layoutWeight = 2.0 - 1.5 * weight;
                    edge.setAttribute("layout.weight", layoutWeight);
                    edge.setAttribute("weight", weight);
                }
            }

            graphs.add(graph);
        }
        return graphs;
    }
}
