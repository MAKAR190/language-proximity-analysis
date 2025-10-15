package com.language_proximity_analysis;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.fxml.FXMLLoader;

public class App extends Application {

    @Override
    public void start(Stage stage) throws Exception {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/main_view.fxml"));
        Scene scene = new Scene(loader.load(), 1000, 700);
        // scene.getStylesheets().add(getClass().getResource("styles.css").toExternalForm());
        stage.setTitle("Graph Visualizer");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }

}