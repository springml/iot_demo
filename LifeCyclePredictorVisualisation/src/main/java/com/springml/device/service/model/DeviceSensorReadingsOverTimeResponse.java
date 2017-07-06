package com.springml.device.service.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.HashMap;

/**
 * Represents Coupon redemption request json
 */
public class DeviceSensorReadingsOverTimeResponse {

    private HashMap<String,HashMap<Long,Double>> deviceSensorReadings;
    private Double latestRulVal;

    public Double getLatestRulVal() {
        return latestRulVal;
    }

    public void setLatestRulVal(Double latestRulVal) {
        this.latestRulVal = latestRulVal;
    }

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
