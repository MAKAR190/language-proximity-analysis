package com.language_proximity_analysis.controller;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.stream.Collectors;

import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;

import com.language_proximity_analysis.graphstream.GraphManager;
import com.language_proximity_analysis.model.TableEntry;
import com.language_proximity_analysis.utils.CellFormatter;
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
    @FXML
    private StackPane analysisView;
    private GraphManager graphManager = GraphManager.getInstance();

    public StackPane getRoot() {
        return analysisView;
    }

    @FXML
    public void initialize() {
        updateTable("en", null);
    }

    public void updateTable(String mainLanguage, String topic) {
        analysisView.getChildren().clear();
        ArrayList<Graph> graphs;
        ArrayList<TableEntry> tableData = new ArrayList<>();
        Graph avgGraph;
        TableEntry avg = new TableEntry("avg");

        if (topic != null) {
            graphs = graphManager.getWordGraphs();
            graphs = graphs.stream().filter(graph -> graph.getAttribute("topic").equals(topic.toLowerCase()))
                    .collect(Collectors.toCollection(ArrayList::new));
            avgGraph = graphManager.findGraph(topic.toLowerCase(), 2);
        } else {
            graphs = graphManager.getTopicGraphs();
            avgGraph = graphManager.findGraph("language", 3);
        }

        for (Node node : avgGraph) {
            if (node.getId().endsWith(mainLanguage)) {
                node.edges().forEach(edge -> {
                    Node opposite = edge.getOpposite(node);
                    String[] idParts = TextFormatter.splitId(opposite.getId());
                    String lang;
                    if (topic != null) {
                        lang = idParts[1];
                    } else {
                        lang = idParts[0];
                    }
                    avg.addProximity(lang, edge.getAttribute("weight", Double.class));
                });
            }
        }

        for (Graph graph : graphs) {
            TableEntry tableEntry = new TableEntry(graph.getId());
            for (Node node : graph) {
                if (node.getId().endsWith(mainLanguage)) {
                    node.edges().forEach(edge -> {
                        Node opposite = edge.getOpposite(node);
                        String lang = TextFormatter.splitId(opposite.getId())[1];
                        tableEntry.addProximity(lang, edge.getAttribute("weight", Double.class));
                    });
                }
            }
            tableData.add(tableEntry);
        }
        TableView<TableEntry> table = new TableView<>();
        TableColumn<TableEntry, String> topicCol;
        if (topic == null) {
            topicCol = new TableColumn<>("Topic");
        } else {
            topicCol = new TableColumn<>("Word");
        }

        topicCol.setCellValueFactory(
                data -> new ReadOnlyStringWrapper(data.getValue().getName()));

        table.getColumns().add(topicCol);

        Set<String> languages = new LinkedHashSet<>();
        for (TableEntry entry : tableData) {
            languages.addAll(entry.getValues().keySet());
        }
        for (String lang : languages) {
            TableColumn<TableEntry, Double> langCol = new TableColumn<>(lang);

            langCol.setCellValueFactory(cell -> {
                Double val = cell.getValue().getValues().get(lang);
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
                    setStyle("-fx-background-color: " + CellFormatter.heatColor(val, avg.getValue(lang)));
                }
            });

            table.getColumns().add(langCol);
        }
        table.setItems(FXCollections.observableArrayList(tableData));
        analysisView.getChildren().add(table);
    }
}
