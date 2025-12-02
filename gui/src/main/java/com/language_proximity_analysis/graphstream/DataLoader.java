package com.language_proximity_analysis.graphstream;

import java.io.FileReader;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class DataLoader {
    public static JsonObject load(String relativePath) throws Exception {
        Path basePath = Paths.get(System.getProperty("user.dir")).getParent(); // project root
        Path jsonPath = basePath.resolve(relativePath);

        return JsonParser.parseReader(new FileReader(jsonPath.toFile())).getAsJsonObject();
    }
}
