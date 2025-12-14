package com.language_proximity_analysis.utils;

public class TextFormatter {
    public static String[] splitId(String word) {
        String[] parts = word.split("_");
        if (parts.length == 2)
            parts[0] = capitalizeFirstLetter(parts[0]);
        return parts;
    }

    public static String capitalizeFirstLetter(String word) {
        return word.substring(0, 1).toUpperCase() + word.substring(1);
    }
}
