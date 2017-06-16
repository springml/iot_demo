package com.springml.device.service.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.ArrayList;

/**
 * Represents Coupon redemption service response json
 */
public class DevicesLifeCyclePredictionResponse {
    @JsonProperty("response")
    private ArrayList<Device> response = new ArrayList<Device>();

    public ArrayList<Device> getResponse() {
        return response;
    }

    public void setResponse(ArrayList<Device> response) {
        this.response = response;
    }

    @Override
    public String toString() {
        return "devices_LifeCycle_PredictionResponse{}";
    }
}
