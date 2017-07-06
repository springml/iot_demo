package com.springml.device.service.model;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by kaarthikraaj on 15/6/17.
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
