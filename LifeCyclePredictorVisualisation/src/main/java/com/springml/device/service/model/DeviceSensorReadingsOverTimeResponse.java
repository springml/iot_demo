package com.springml.device.service.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.HashMap;

/**
 * Represents Coupon redemption request json
 */
public class DeviceSensorReadingsOverTimeResponse {

    private HashMap<String,HashMap<Long,Double>> deviceSensorReadings;

    public HashMap<String, HashMap<Long, Double>> getDeviceSensorReadings() {
        return deviceSensorReadings;
    }

    public void setDeviceSensorReadings(HashMap<String, HashMap<Long, Double>> deviceSensorReadings) {
        this.deviceSensorReadings = deviceSensorReadings;
    }

    @Override
    public String toString() {
        return "deviceSensorReadings";
    }
}
