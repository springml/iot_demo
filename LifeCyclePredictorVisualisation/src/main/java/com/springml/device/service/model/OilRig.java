package com.springml.device.service.model;

/**
 * Created by kaarthikraaj on 15/6/17.
 */
public class OilRig {
    String name;
    Double latitude;
    Double Longtitude;
    Double remainingLifeCycle;



    public Double getRemainingLifeCycle() {
        return remainingLifeCycle;
    }

    public void setRemainingLifeCycle(Double remainingLifeCycle) {
        this.remainingLifeCycle = remainingLifeCycle;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getLongtitude() {
        return Longtitude;
    }

    public void setLongtitude(Double longtitude) {
        Longtitude = longtitude;
    }

    public String getName() {

        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String toString(){
        return "Name:"+this.name + " - Lat"+this.latitude+"-Long"+this.getLongtitude();
    }
}
