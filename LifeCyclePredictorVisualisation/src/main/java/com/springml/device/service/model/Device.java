package com.springml.device.service.model;

/**
 * Created by kaarthikraaj on 15/6/17.
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
