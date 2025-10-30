package com.language_proximity_analysis.graphstream;

public class TextFormatter {
    public static String toLabel(String word){
        word = word.substring(0, word.indexOf('_'));
        return capitalizeFirstLetter(word);
    }

    public static String capitalizeFirstLetter(String word){
        return word.substring(0,1).toUpperCase() + word.substring(1);
    }
}
