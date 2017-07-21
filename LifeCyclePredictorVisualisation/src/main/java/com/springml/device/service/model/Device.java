package com.springml.device.service.model;

/**
 * Represents individual unit of response for getDeviceLifecyclePredictions service
 */
public class Device {
    String name;

    public Double getRulVal() {
        return rulVal;
    }

    public void setRulVal(Double rulVal) {
        this.rulVal = rulVal;
    }

    Double rulVal;
    long cycle;

    public long getCycle() {
        return cycle;
    }

    public void setCycle(long cycle) {
        this.cycle = cycle;
    }

    public String getName() {

        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

}
