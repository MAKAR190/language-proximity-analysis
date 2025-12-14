package com.language_proximity_analysis.utils;

import javafx.scene.paint.Color;

public class CellFormatter {
    public static String heatColor(double value, double avg) {

        // Normalize to [-1 .. 1]
        double maxDist = Math.max(avg, 1.0 - avg);
        double norm = (value - avg) / maxDist;
        norm = Math.max(-1, Math.min(1, norm));

        Color color;

        if (norm < 0) {
            // Blue → White
            double t = norm + 1; // [-1..0] → [0..1]
            color = Color.hsb(
                    210, // blue hue
                    1.0 - t, // desaturate toward white
                    1.0);
        } else {
            // White → Orange/Red
            double t = norm; // [0..1]
            color = Color.hsb(
                    30, // orange-red hue (no pink)
                    t,
                    1.0);
        }

        return toRgb(color);
    }

    private static String toRgb(Color c) {
        return String.format(
                "rgb(%d,%d,%d)",
                (int) (c.getRed() * 255),
                (int) (c.getGreen() * 255),
                (int) (c.getBlue() * 255));
    }
}
