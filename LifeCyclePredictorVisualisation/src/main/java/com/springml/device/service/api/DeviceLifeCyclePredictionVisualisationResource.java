package com.springml.device.service.api;

import com.springml.device.service.model.DeviceSensorReadingsOverTimeResponse;
import com.springml.device.service.model.DevicesLifeCyclePredictionResponse;
import com.springml.device.service.model.OilRigsResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Rest controller class for redeem coupon service
 * Two resources defined
 * a) / and b) /redeemCoupon
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

    /* defines the resource responsible for redeeming coupon
       @param redeemCouponRequest redeem coupon request representing json
        @return  DevicesLifeCyclePredictionResponse which will be converted to json
     */

    @CrossOrigin
    @RequestMapping(value = "/getDeviceLifecyclePredictions", method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<DevicesLifeCyclePredictionResponse> getDeviceLifecyclePredictions(@RequestParam String oilRigId,@RequestParam double latitude,@RequestParam double longtitude,@RequestParam int durationInMins) {
        return ResponseEntity.ok(deviceLifecyclePredictionVisualisationServer.getDeviceLifecyclePredictions( oilRigId,latitude,longtitude,durationInMins));
    }

    @CrossOrigin
    @RequestMapping(value = "/getSensorReadingsForDevice", method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<DeviceSensorReadingsOverTimeResponse> getSensorReadingsForDevice(@RequestParam String industrialPlantId,@RequestParam String deviceId,@RequestParam int durationInMins) {

        return ResponseEntity.ok(deviceLifecyclePredictionVisualisationServer.getSensorReadingsForDevice(industrialPlantId,deviceId,durationInMins));

    }

    @CrossOrigin
    @RequestMapping(value = "/getOilRigs", method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<OilRigsResponse> getOilRigs(@RequestParam int durationInMins) {

        return ResponseEntity.ok(deviceLifecyclePredictionVisualisationServer.getOilRigs(durationInMins));

    }
}
