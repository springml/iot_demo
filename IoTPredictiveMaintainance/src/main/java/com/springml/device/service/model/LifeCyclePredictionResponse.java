package com.springml.device.service.model;

/**
 * This the the LifeCyclePredictionResponse class that is the pojo instance
 * of json output from DeviceLifeCyclePredictor ML API
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
