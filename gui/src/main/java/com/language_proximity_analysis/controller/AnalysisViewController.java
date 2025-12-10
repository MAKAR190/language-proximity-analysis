package com.language_proximity_analysis.controller;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.Set;

import org.graphstream.graph.Edge;
import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;

import com.language_proximity_analysis.graphstream.GraphManager;
import com.language_proximity_analysis.model.TopicTableEntry;
import com.language_proximity_analysis.utils.TextFormatter;

import javafx.beans.property.ReadOnlyObjectWrapper;
import javafx.beans.property.ReadOnlyStringWrapper;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.TableCell;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.layout.StackPane;

public class AnalysisViewController {
    // TO DO:
    // heatmap
    // select topic, select main language
    // rows - words, columns - languages
    // comparison to average value for given language pair
    @FXML
    private StackPane analysisView;
    private GraphManager graphManager = GraphManager.getInstance();

    public StackPane getRoot() {
        return analysisView;
    }

    // public void updateInfo(String id, String mainLanguage){
    // boolean topicLevel = true;
    // if(topicLevel){
    // Graph graph = graphManager.findGraph(id, 2);
    // for(Node node:graph){
    // node.getId()
    // }
    // TopicTableEntry topicTableEntry = new TopicTableEntry();

    // }
    // }

    // for topics
    public void updateInfo(String mainLanguage) {
        analysisView.getChildren().clear();
        ArrayList<TopicTableEntry> tableData = new ArrayList<>();
        ArrayList<Graph> graphs = graphManager.getTopicGraphs();
        for (Graph graph : graphs) {
            TopicTableEntry topicTableEntry = new TopicTableEntry(graph.getId());
            for (Node node : graph) {
                if (node.getId().endsWith(mainLanguage)) {
                    node.edges().forEach(edge -> {
                        Node opposite = edge.getOpposite(node);
                        String lang = TextFormatter.splitId(opposite.getId())[1];
                        topicTableEntry.addProximity(lang, edge.getAttribute("weight", Double.class));
                    });
                }
            }
            tableData.add(topicTableEntry);
        }

        TableView<TopicTableEntry> table = new TableView<>();
        TableColumn<TopicTableEntry, String> topicCol = new TableColumn<>("Topic");

        topicCol.setCellValueFactory(
                data -> new ReadOnlyStringWrapper(data.getValue().getTopic()));

        table.getColumns().add(topicCol);

        Set<String> languages = new LinkedHashSet<>();
        for (TopicTableEntry entry : tableData) {
            languages.addAll(entry.getProximity().keySet());
        }
        for (String lang : languages) {
            TableColumn<TopicTableEntry, Double> langCol = new TableColumn<>(lang);

            langCol.setCellValueFactory(cell -> {
            Double val = cell.getValue().getProximity().get(lang);
            return new ReadOnlyObjectWrapper<>(val);
            });

            langCol.setCellFactory(col -> new TableCell<>() {
                @Override
                protected void updateItem(Double val, boolean empty) {
                    super.updateItem(val, empty);

                    if (empty || val == null) {
                        setText(null);
                        setStyle(""); // reset style
                        return;
                    }

                    setText(String.format("%.3f", val));

                    if (val < 0.5)
                        setStyle("-fx-background-color: lightcoral;");
                    else if (val >= 0.8)
                        setStyle("-fx-background-color: lightgreen;");
                    else
                        setStyle(""); // default
                }
            });

            table.getColumns().add(langCol);
        }
        table.setItems(FXCollections.observableArrayList(tableData));
        analysisView.getChildren().add(table);
    }
}
