package com.springml.device.service.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.HashMap;

/**
 * Represents Coupon redemption request json
 */
public class DeviceSensorReadingsOverTimeResponse {

    private HashMap<String,HashMap<String,Double>> deviceSensorReadings;

    public HashMap<String, HashMap<String, Double>> getDeviceSensorReadings() {
        return deviceSensorReadings;
    }

    public void setDeviceSensorReadings(HashMap<String, HashMap<String, Double>> deviceSensorReadings) {
        this.deviceSensorReadings = deviceSensorReadings;
    }

    @Override
    public String toString() {
        return "deviceSensorReadings";
    }
}
