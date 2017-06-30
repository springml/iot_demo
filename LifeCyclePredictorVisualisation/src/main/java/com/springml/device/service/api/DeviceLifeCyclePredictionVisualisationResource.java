package com.springml.device.service.api;

import com.springml.device.service.model.DeviceSensorReadingsOverTimeResponse;
import com.springml.device.service.model.DevicesLifeCyclePredictionResponse;
import com.springml.device.service.model.OilRigsResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Rest controller class for Device LifeCyle Prediction Visualisation service
 * Four resources defined
 * a)homepage
 * b)getDeviceLifecyclePredictions
 * c)getSensorReadingsForDevice
 * d)getOilRigs
 */
@RestController
public class DeviceLifeCyclePredictionVisualisationResource {
    @Autowired
    DeviceLifecyclePredictionVisualisationServer deviceLifecyclePredictionVisualisationServer;

    /* defines home page url
     */
    @CrossOrigin
    @RequestMapping(value = "/", method = RequestMethod.GET)
    public String home() {
        return "Device Lifecycle Prediction Visualtion Service is running!";
    }

    /* defines the resource responsible for getting list of devices and
        its predicted remaining life cycles
       @param oilRigId Industrial plant id which is he identifies an oilrig location
       @param latitude  latitude of an oilrig instance
       @param longtitude  longtitude of an oilrig instance
        @param durationInMins the records are fetched for the duration passed
        and its in mins
        @return  DevicesLifeCyclePredictionResponse which will be converted to json
     */

    @CrossOrigin
    @RequestMapping(value = "/getDeviceLifecyclePredictions", method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<DevicesLifeCyclePredictionResponse> getDeviceLifecyclePredictions(@RequestParam String oilRigId, @RequestParam double latitude, @RequestParam double longtitude, @RequestParam int durationInMins) {
        return ResponseEntity.ok(deviceLifecyclePredictionVisualisationServer.getDeviceLifecyclePredictions(oilRigId, latitude, longtitude, durationInMins));
    }

    /* defines the resource responsible for getting list of sensor readings for the device id passeds predicted remaining life cycles
       @param industrialPlantId Industrial plant id which is he identifies an oilrig location
       @param deviceId  identifies the device for which the sensor readings are requested
       @param durationInMins the records are fetched for the duration passed
        and its in mins
       @return  DeviceSensorReadingsOverTimeResponse which will be converted to json
     */
    @CrossOrigin
    @RequestMapping(value = "/getSensorReadingsForDevice", method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<DeviceSensorReadingsOverTimeResponse> getSensorReadingsForDevice(@RequestParam String industrialPlantId, @RequestParam String deviceId, @RequestParam int durationInMins) {

        return ResponseEntity.ok(deviceLifecyclePredictionVisualisationServer.getSensorReadingsForDevice(industrialPlantId, deviceId, durationInMins));

    }

    /* defines the resource responsible for getting list of oil rigs instances and its location details

           @param durationInMins the records are fetched for the duration passed
            and its in mins
           @return  OilRigsResponse which will be converted to json
         */
    @CrossOrigin
    @RequestMapping(value = "/getOilRigs", method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<OilRigsResponse> getOilRigs(@RequestParam int durationInMins) {

        return ResponseEntity.ok(deviceLifecyclePredictionVisualisationServer.getOilRigs(durationInMins));

    }
}
