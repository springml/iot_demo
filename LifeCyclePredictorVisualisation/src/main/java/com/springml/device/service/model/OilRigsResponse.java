package com.springml.device.service.model;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * This class represents response for get oilrig service
 * This instance is converted to json and sent back as response
 */
public class OilRigsResponse {
    private ArrayList<OilRig> oilRigs = new ArrayList<OilRig>();

    public ArrayList<OilRig> getOilRigs() {
        return oilRigs;
    }

    public void setOilRigs(ArrayList<OilRig> oilRigs) {
        this.oilRigs = oilRigs;
    }

    @Override
    public String toString() {
        return "oilRigsResponse{}";
    }
}
