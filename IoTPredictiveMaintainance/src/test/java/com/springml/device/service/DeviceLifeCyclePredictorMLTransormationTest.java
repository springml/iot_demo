package com.springml.device.service;

import com.google.api.services.bigquery.model.TableRow;
import com.google.cloud.dataflow.sdk.options.PipelineOptionsFactory;
import org.junit.Test;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Properties;

import static org.junit.Assert.assertNotEquals;


/**
 * This the the junit test file for DeviceLifeCyclePredictorMLTransform
 * that  is responsible for testing
 * ML API and asserting the response
 */
public class DeviceLifeCyclePredictorMLTransormationTest {

    @Test
    public void testLifeCyclePredictorTransformation() {
        Properties argsProperties = new Properties();
        try {
            argsProperties.load(new FileReader(new File("application.properties")));
        } catch (IOException e) {
            e.printStackTrace();
        }
        String argsOptions = argsProperties.getProperty("args");
        String[] args = argsOptions.split(",");

        DeviceLifeCyclePredictorPipelineOptions options =
                PipelineOptionsFactory.fromArgs(args).withValidation().as(DeviceLifeCyclePredictorPipelineOptions.class);
        String mlUrl = options.getIotPredictiveMaintainanceMLUrl();
        DeviceLifeCyclePredictorMLTransormation deviceLifeCyclePredictorMLTransormation = new DeviceLifeCyclePredictorMLTransormation(mlUrl);

        TableRow tableRow = new TableRow();
        tableRow.set("UnitNumber", 101);
        tableRow.set("Cycle", 101);
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
        tableRow.set("OpSet3", 101);
        tableRow.set("OpSet2", 101);
        tableRow.set("OpSet1", 101);
        TableRow response = deviceLifeCyclePredictorMLTransormation.getPredictedLifeCycle(tableRow);
        assertNotEquals(-99999, response.get("RemainingOperationCycles"));
    }
}
