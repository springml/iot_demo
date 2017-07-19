package com.springml.device.service.api;

import com.springml.device.service.model.DeviceSensorReadingsOverTimeResponse;
import com.springml.device.service.model.DevicesLifeCyclePredictionResponse;
import com.springml.device.service.model.OilRig;
import com.springml.device.service.model.OilRigsResponse;
import org.springframework.beans.factory.annotation.Autowired;

import java.sql.Date;
import java.time.LocalDateTime;
import java.util.ArrayList;

/**
 * Device LifecyclePrediction Visualisation Server that has main apis
 * used by Device LifeCycle Prediction visualisation layer
 */
public class DeviceLifecyclePredictionVisualisationServer {
    @Autowired
    OilRigsDevicesManager oilRigsDevicesManager;


    public DevicesLifeCyclePredictionResponse getDeviceLifecyclePredictions(String oilRigId, double latitude, double longtitude, int durationInMins) {
        System.out.println("Start time of getlifecycleprediction"+LocalDateTime.now());
        DevicesLifeCyclePredictionResponse devicesLifeCyclePredictionResponse = new DevicesLifeCyclePredictionResponse();
        devicesLifeCyclePredictionResponse.setResponse(oilRigsDevicesManager.getDevicesLifeCyclePredictions(oilRigId, latitude, longtitude, durationInMins));
        System.out.println("End time of getlifecycleprediction"+ LocalDateTime.now());

        return devicesLifeCyclePredictionResponse;

    }

    public DeviceSensorReadingsOverTimeResponse getSensorReadingsForDevice(String industrialPlantId, String deviceId, int durationInMins) {

        return oilRigsDevicesManager.getOilRigDeviceSensorReadings(industrialPlantId, deviceId, durationInMins);
    }

    public OilRigsResponse getOilRigs(int durationInMins) {

        OilRigsResponse oilRigsResponse = new OilRigsResponse();
        ArrayList<OilRig> oilrigs = oilRigsDevicesManager.getOilRigs(durationInMins);
        oilRigsResponse.setOilRigs(oilrigs);
        return oilRigsResponse;
    }


}
