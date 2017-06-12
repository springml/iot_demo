package com.springml.device.service;

import com.google.api.client.http.json.JsonHttpContent;
import com.google.api.client.json.jackson.JacksonFactory;
import com.google.api.services.bigquery.model.TableRow;
import com.google.cloud.dataflow.sdk.transforms.DoFn;
import com.springml.device.service.model.LifeCyclePredictionResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.AddressException;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import java.io.ByteArrayOutputStream;
import java.io.UnsupportedEncodingException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.*;

/**
 * The transformation  is responsible for calling
 * DeviceLifeCyclePredictor ML API and add the response to the pipeline
 */
public class DeviceLifeCyclePredictorMLTransormation extends DoFn<TableRow, TableRow> {
    private static final Logger LOG = LoggerFactory.getLogger(DeviceLifeCyclePredictorMLTransormation.class);
    //DeviceLifeCylclePredictor Rest ML API client
    DeviceLifeCyclePredictorClient deviceLifeCyclePredictorClient = new DeviceLifeCyclePredictorClient();
    //DeviceLifeCylclePredictor Rest ML URL
    private String fleetPreventiveMLUrl;


    public DeviceLifeCyclePredictorMLTransormation(String fleetPreventiveMLUrl) {
        this.fleetPreventiveMLUrl = fleetPreventiveMLUrl;
    }

    public static void main(String args[]) {
        DeviceLifeCyclePredictorMLTransormation client = new DeviceLifeCyclePredictorMLTransormation("https://ml.googleapis.com/v1beta1/projects/mlpdm-168115/models/predictivemaintenance_v3/versions/v3:predict");
        TableRow tableRow = new TableRow();
        tableRow.set("UnitNumber", "101");
        tableRow.set("Cycle", 101);
        tableRow.set("OpSet1", 101);
        tableRow.set("OpSet2", 101);
        tableRow.set("OpSet3", 101);
        tableRow.set("SensorMeasure1", 101);
        tableRow.set("SensorMeasure2", 101);
        tableRow.set("SensorMeasure3", 101);
        tableRow.set("SensorMeasure4", 101);
        tableRow.set("SensorMeasure5", 101);
        tableRow.set("SensorMeasure6", 101);
        tableRow.set("SensorMeasure7", 101);
        tableRow.set("SensorMeasure8", 101);
        tableRow.set("SensorMeasure9", 101);
        tableRow.set("SensorMeasure10", 101);
        tableRow.set("SensorMeasure11", 101);
        tableRow.set("SensorMeasure12", 101);
        tableRow.set("SensorMeasure13", 101);
        tableRow.set("SensorMeasure14", 101);
        tableRow.set("SensorMeasure15", 101);
        tableRow.set("SensorMeasure16", 101);
        tableRow.set("SensorMeasure17", 101);
        tableRow.set("SensorMeasure18", 101);
        tableRow.set("SensorMeasure19", 101);
        tableRow.set("SensorMeasure20", 101);
        tableRow.set("SensorMeasure21", 101);

        TableRow response = client.getPredictedLifeCycle(tableRow);
        LOG.info("The response prediction is" + response.get("RemainingOperationCycles"));
    }


    private TableRow getTableRowFromResponse(LifeCyclePredictionResponse predictionResponse, TableRow responseRow) {
        try {
            float remainingOperationCycles = predictionResponse.getPredictions()[0].getOutputs();
            if(remainingOperationCycles < 121 ) {
                LOG.warn("RemainingOperationCycles threshold reached for device with Unit Number"+responseRow.get("UnitNumber")+" The RUL Value is "+remainingOperationCycles);
            }
            responseRow.set("RemainingOperationCycles", remainingOperationCycles);
            responseRow.set("PredictedDate",  LocalDateTime.now().toString());
        } catch (Exception e) {
            responseRow.set("RemainingOperationCycles", -99999);
            responseRow.set("PredictedDate",  LocalDateTime.now());
            LOG.info("Exception while parsing response" + e.getMessage().toString());
        }
        return responseRow;
    }

    /*
    The method is responsible for generating Map out of input data from pipeline
    The Map will be converted to JSON before sending request to ML API
     */
    private Object getAsCloudMLRequest(TableRow sensorDetails) {
        List<Map<String, Object>> instances = new ArrayList<>();
        Map<String, Object> map = new HashMap<>();
        map.put("Cycle", sensorDetails.get("Cycle"));
        map.put("OpSet1", sensorDetails.get("OpSet1"));
        map.put("OpSet2", sensorDetails.get("OpSet2"));
        map.put("OpSet3", sensorDetails.get("OpSet3"));
        map.put("SensorMeasure1", sensorDetails.get("SensorMeasure1"));
        map.put("SensorMeasure2", sensorDetails.get("SensorMeasure2"));
        map.put("SensorMeasure3", sensorDetails.get("SensorMeasure3"));
        map.put("SensorMeasure4", sensorDetails.get("SensorMeasure4"));
        map.put("SensorMeasure5", sensorDetails.get("SensorMeasure5"));
        map.put("SensorMeasure6", sensorDetails.get("SensorMeasure6"));
        map.put("SensorMeasure7", sensorDetails.get("SensorMeasure7"));
        map.put("SensorMeasure8", sensorDetails.get("SensorMeasure8"));
        map.put("SensorMeasure9", sensorDetails.get("SensorMeasure9"));
        map.put("SensorMeasure10", sensorDetails.get("SensorMeasure10"));
        map.put("SensorMeasure11", sensorDetails.get("SensorMeasure11"));
        map.put("SensorMeasure12", sensorDetails.get("SensorMeasure12"));
        map.put("SensorMeasure13", sensorDetails.get("SensorMeasure13"));
        map.put("SensorMeasure14", sensorDetails.get("SensorMeasure14"));
        map.put("SensorMeasure15", sensorDetails.get("SensorMeasure15"));
        map.put("SensorMeasure16", sensorDetails.get("SensorMeasure16"));
        map.put("SensorMeasure17", sensorDetails.get("SensorMeasure17"));
        map.put("SensorMeasure18", sensorDetails.get("SensorMeasure18"));
        map.put("SensorMeasure19", sensorDetails.get("SensorMeasure19"));
        map.put("SensorMeasure20", sensorDetails.get("SensorMeasure20"));
        map.put("SensorMeasure21", sensorDetails.get("SensorMeasure21"));

        instances.add(map);
        return instances;
    }

    public void processElement(ProcessContext c) throws Exception {

        TableRow tableRow = c.element();
        c.output(getPredictedLifeCycle(tableRow));
    }

    /*
    The method is responsible for calling ML API
     */
    protected TableRow getPredictedLifeCycle(TableRow sensorDetails) {
        TableRow responseRow = new TableRow();

        try {

            JacksonFactory jacksonFactory = new JacksonFactory();
            JsonHttpContent jsonHttpContent = new JsonHttpContent(jacksonFactory, getAsCloudMLRequest(sensorDetails));

            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            jsonHttpContent.setWrapperKey("instances");
            LifeCyclePredictionResponse predictionResponse = deviceLifeCyclePredictorClient.getPredictedLifeCycle(jsonHttpContent, fleetPreventiveMLUrl);

            return getTableRowFromResponse(predictionResponse, sensorDetails);
        } catch (Exception exc) {
            LOG.error("Error while getting predictions using CloudML", exc.getMessage());
        }

        return responseRow;
    }



}
