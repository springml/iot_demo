package com.springml.device.service.model;

/**
 * Created by kaarthikraaj on 6/6/17.
 */
public class LifeCyclePredictionResponse {
     Predictions[] predictions;

    public Predictions[] getPredictions() {
        return predictions;
    }

    public void setPredictions(Predictions[] predictions) {
        this.predictions = predictions;
    }
}
