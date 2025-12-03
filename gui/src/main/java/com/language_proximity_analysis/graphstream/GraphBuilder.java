package com.language_proximity_analysis.graphstream;

import java.util.ArrayList;
import java.util.Map;

import org.graphstream.graph.Edge;
import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.implementations.SingleGraph;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.language_proximity_analysis.utils.TextFormatter;

public class GraphBuilder {

    public static ArrayList<Graph> buildGraphsFromJson(JsonObject root) {
        ArrayList<Graph> graphs = new ArrayList<>();
        for (Map.Entry<String, JsonElement> entry : root.entrySet()) {
            String graphId = entry.getKey().toLowerCase();
            JsonObject graphData = entry.getValue().getAsJsonObject();
            Graph graph = new SingleGraph(graphId);
            for (JsonElement nodeEl : graphData.getAsJsonArray("nodes")) {
                JsonObject nodeData = nodeEl.getAsJsonObject();

                String id = nodeData.get("id").getAsString();
                Node node = graph.addNode(id);

                String[] parts = TextFormatter.splitId(id);
                if (parts.length == 2) {
                    node.setAttribute("ui.label", parts[0]);
                    node.setAttribute("ui.class", parts[1]);
                } else {
                    node.setAttribute("ui.class", parts[0]);
                }
            }

            for (JsonElement edgeEl : graphData.getAsJsonArray("edges")) {
                JsonObject edgeData = edgeEl.getAsJsonObject();

                String source = edgeData.get("source").getAsString();
                String target = edgeData.get("target").getAsString();
                String edgeId = source + "_" + target;
                Edge edge = graph.addEdge(edgeId, source, target, false); // undirected

                if (edgeData.has("weight")) {
                    double weight = edgeData.get("weight").getAsDouble();
                    String formattedWeight = String.format("%.2f", weight);
                     edge.setAttribute("ui.label", formattedWeight);
                    edge.setAttribute("ui.size", weight * 10);
                    // layoutWeight is multiplier for edge length
                    // default is 1, larger = longer edge, smaller = shorter edge
                    // our weight works opposite way, so we invert it and remap 0.0-1.0 into 0.5-2.0
                    double layoutWeight = 2.0 - 1.5 * weight;
                    edge.setAttribute("layout.weight", layoutWeight);
                    edge.setAttribute("weight", weight);

                    if (weight == 1.0) {
                        edge.setAttribute("ui.class", "identical");
                    } else if (weight == 0.0) {
                        edge.setAttribute("ui.class", "unrelated");
                    } else if (weight > 0.5) {
                        edge.setAttribute("ui.class", "similar");
                    } else {
                        edge.setAttribute("ui.class", "different");
                    }
                }
            }

            graphs.add(graph);
        }
        return graphs;
    }
}
