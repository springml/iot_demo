package com.springml.device.service.api;

import com.google.gson.Gson;
import com.springml.device.service.model.DeviceSensorReadingsOverTimeResponse;
import com.springml.device.service.model.DevicesLifeCyclePredictionResponse;
import com.springml.device.service.model.OilRig;
import com.springml.device.service.model.OilRigsResponse;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;

/**
 * Coupon redeem server that has main api that gets invoked
 * coupon redeem action is performed
 */
public class DeviceLifecyclePredictionVisualisationServer {



    public DevicesLifeCyclePredictionResponse getDeviceLifecyclePredictions(String oilRigId,double latitude,double longtitude, int durationInMins) {
        DevicesLifeCyclePredictionResponse devicesLifeCyclePredictionResponse = new DevicesLifeCyclePredictionResponse();
        devicesLifeCyclePredictionResponse.setResponse(OilRigsDevicesManager.getDevicesLifeCyclePredictions(oilRigId,latitude,longtitude,durationInMins));
        return devicesLifeCyclePredictionResponse;

    }

    public DeviceSensorReadingsOverTimeResponse getSensorReadingsForDevice(String industrialPlantId,String deviceId, int durationInMins) {

        return OilRigsDevicesManager.getOilRigDeviceSensorReadings(industrialPlantId,deviceId,durationInMins);
    }

    public OilRigsResponse getOilRigs( int durationInMins){
        OilRigsResponse oilRigsResponse = new OilRigsResponse();
        ArrayList<OilRig> oilrigs = OilRigsDevicesManager.getOilRigs(durationInMins);
        oilRigsResponse.setOilRigs(oilrigs);
        return oilRigsResponse;
    }

    public static void main(String args[]){
        DeviceLifecyclePredictionVisualisationServer deviceLifecyclePredictionVisualisationServer = new DeviceLifecyclePredictionVisualisationServer();
        Gson gson = new Gson();

        ArrayList<OilRig> oilRigs = OilRigsDevicesManager.getOilRigs(12*60);
        for(OilRig oilRig: oilRigs) {
            DevicesLifeCyclePredictionResponse response = deviceLifecyclePredictionVisualisationServer.getDeviceLifecyclePredictions(oilRig.getName(),oilRig.getLatitude(),oilRig.getLongtitude(),720);

            String jsonResponse = gson.toJson(response, DevicesLifeCyclePredictionResponse.class);
            System.out.println("The oil rig returned is "+oilRig.getName() +"and its device list and RULS are "+jsonResponse);
        }

  //      DeviceSensorReadingsOverTimeResponse deviceSensorReadingsOverTimeResponse = deviceLifecyclePredictionVisualisationServer.getSensorReadingsForDevice("IndustrialPlant0","Unit_1");
    //    String sensorReadingsResponse = gson.toJson(deviceSensorReadingsOverTimeResponse,DeviceSensorReadingsOverTimeResponse.class);
      //  System.out.println("The sensor readings for the device passed is"+ sensorReadingsResponse);


    }
}
