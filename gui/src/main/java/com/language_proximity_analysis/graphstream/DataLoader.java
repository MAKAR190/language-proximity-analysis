package com.language_proximity_analysis.graphstream;

import java.io.FileReader;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class DataLoader {
    public static JsonObject load(String filename) throws Exception {
        return JsonParser.parseReader(new FileReader(filename)).getAsJsonObject();
    }
}
