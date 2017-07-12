package com.springml.device.service.api;

import com.google.cloud.WaitForOption;
import com.google.cloud.bigquery.*;
import com.springml.device.service.model.Device;
import com.springml.device.service.model.DeviceSensorReadingsOverTimeResponse;
import com.springml.device.service.model.OilRig;
import org.springframework.beans.factory.annotation.Value;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.logging.Logger;

/**
 * This class is responsible for all query (bigquery) operations that corresponds to
 * every action performed in the LifeCycle Predictor UI
 * It totally has three queries
 * a)query to get OilRigs
 * b)query to get devices and its Remaining LifeCycle value
 * for the given OilRig instance
 * c)query to get all sensor readings for a particular device
 * for the configured duration
 */
public class OilRigsDevicesManager {
    private static Logger logger =
            Logger.getLogger(OilRigsDevicesManager.class.getName());
    private static long count = 0;
    private static BigQuery bigQueryClient;
    private static ArrayList<OilRig> oilRigs = new ArrayList<OilRig>();

    static {
        bigQueryClient = createAuthorizedClient();
    }

    @Value("${lifecycle.prediction.tableName}")
    private String tableName;

    /*
        Prepares for authorization to build BigQuery Client
    */
    private static BigQuery createAuthorizedClient() {
        BigQuery bigQueryClient = null;

        try {
            bigQueryClient = BigQueryOptions.getDefaultInstance().getService();
        } catch (Exception exception) {
            logger.severe("Exception while preparing for authorization :" + exception.getMessage());
        }

        return bigQueryClient;
    }

    /**
     * The method is responsible for fetching list of oilrigs from bigquery along
     * with its lat and longtitude locations
     */
    public ArrayList<OilRig> getOilRigs(int durationInMins) {
        ArrayList<OilRig> oilRigs = new ArrayList<OilRig>();
        //callbigquery to get list of IndustrialPlants and form array list
        String industrialPlantsQuery = generateIndustrialPlantsQuery(getFromDate(durationInMins));
        System.out.println("the query is " + industrialPlantsQuery);
        Job industrialPlantsJob = createJob(industrialPlantsQuery, bigQueryClient);
        waitForJobCompletion(industrialPlantsJob);
        QueryResponse response = bigQueryClient.getQueryResults(industrialPlantsJob.getJobId());
        QueryResult result = processResponseAndGetResult(response);
        Iterator<List<FieldValue>> rowItr = result.iterateAll().iterator();

        while (rowItr.hasNext()) {
            List<FieldValue> columns = rowItr.next();
            OilRig oilRig = new OilRig();

            for (int loopCount = 0; loopCount < columns.size(); loopCount++) {
                if (loopCount == 0) {
                    oilRig.setName(columns.get(loopCount).getStringValue());
                } else {
                    if (loopCount == 1) {
                        oilRig.setLatitude(columns.get(loopCount).getDoubleValue());
                    } else {
                        if (loopCount == 2) {
                            oilRig.setLongtitude(columns.get(loopCount).getDoubleValue());
                        }
                        else {
                            if (loopCount == 3) {
                                oilRig.setRemainingLifeCycle(columns.get(loopCount).getDoubleValue());
                            }
                        }
                    }
                }

            }
            oilRigs.add(oilRig);
        }
        return oilRigs;

    }

    private void waitForJobCompletion(Job job) {
        try {
            job.waitFor(WaitForOption.checkEvery(1, TimeUnit.SECONDS));

        } catch (InterruptedException | TimeoutException e) {
            e.printStackTrace();
        }
    }

    private Job createJob(String query, BigQuery bigQueryClient) {
        QueryJobConfiguration.Builder queryJobBuilder = QueryJobConfiguration.newBuilder(query);
        QueryJobConfiguration jobConfig = queryJobBuilder.build();

        JobInfo.Builder builder = Job.newBuilder(jobConfig);
        JobInfo jobInfo = builder.build();
        Job job = bigQueryClient.create(jobInfo);
        return job;
    }

    private QueryResult processResponseAndGetResult(QueryResponse response) {
        QueryResult result = null;
        List<BigQueryError> executionErrors = response.getExecutionErrors();
        // look for errors in executionErrors
        if (executionErrors.isEmpty()) {
            result = response.getResult();
            logger.info("Query Execution Successful");
        } else {
            StringBuilder errorMsg = new StringBuilder();
            for (BigQueryError err : executionErrors) {
                errorMsg.append(err.getMessage()).append('\n');
            }
            logger.severe("Error while executing bigquery job" + errorMsg.toString());
        }
        return result;
    }

    private String generateIndustrialPlantsQuery(String fromDate) {
        String fetchIndustrialPlantsQuery = "SELECT IndustrialPlantName,Latitude,Longtitude,min(RemainingOperationCycles) as RUL FROM [" + tableName + "] where IndustrialPlantName is not null and PredictedDate >  DATETIME(\"" + fromDate + "\")  group by  \n" +
                "IndustrialPlantName,Latitude,Longtitude\n";

        return fetchIndustrialPlantsQuery;
    }

    private String fetchDeviceAndLatestPreditionsQuery(String industrialPlantName, double latitude, double longtitude, String fromDate) {
        String fetchIndustrialPlantsQuery = "SELECT UnitNumber,RemainingOperationCycles from (SELECT   RemainingOperationCycles,Cycle,UnitNumber as deviceId,IndustrialPlantName as plant from [" + tableName + "]  where IndustrialPlantName like '" + industrialPlantName + "' AND Latitude=" + latitude + " AND Longtitude=" + longtitude + " and PredictedDate >  DATETIME(\"" + fromDate + "\") \n)  FirstTable JOIN (SELECT Max(Cycle) AS MaxCycle,UnitNumber,IndustrialPlantName\n" +
                "FROM \n" +
                "[" + tableName + "]\n" +
                "WHERE Cycle is NOT NULL AND IndustrialPlantName like '" + industrialPlantName + "' AND Latitude=" + latitude + " AND Longtitude=" + longtitude + " and PredictedDate >  DATETIME(\"" + fromDate + "\")\n" +
                "group by UnitNumber,IndustrialPlantName ) SecondTable \n" +
                "on FirstTable.deviceId = SecondTable.UnitNumber AND  FirstTable.plant = SecondTable.IndustrialPlantName AND FirstTable.Cycle=SecondTable.MaxCycle\n";
        return fetchIndustrialPlantsQuery;
    }

    /**
     * The method is responsible for fetching list of sensors and its readings for the device
     * being monitored which is part of the oil rig idenitfied by IndustrialPlant ID
     * from bigquery along
     * with its lat and longtitude locations
     */
    public DeviceSensorReadingsOverTimeResponse getOilRigDeviceSensorReadings(String industrialPlantId, String deviceId, int durationInMins) {
        //query sensor readings for all sensors for the given device from big query table and fill the map
        HashMap<String, HashMap<Long, Double>> sensorsHistoryMap = new HashMap<String, HashMap<Long, Double>>();
        Double latestRulVal = 0d;
        String sensorReadingsQuery = fetchSensorReadingsForDeviceQuery(industrialPlantId, deviceId, getFromDate(durationInMins));
        Job sensorReadingsJob = createJob(sensorReadingsQuery, bigQueryClient);
        waitForJobCompletion(sensorReadingsJob);
        QueryResponse response = bigQueryClient.getQueryResults(sensorReadingsJob.getJobId());
        QueryResult result = processResponseAndGetResult(response);
        Iterator<List<FieldValue>> rowItr = result.iterateAll().iterator();
        HashMap<Long, Double> sensorReadingsOverTimeMapForSensorOne = new HashMap<Long, Double>();
        HashMap<Long, Double> sensorReadingsOverTimeMapForSensorTwo = new HashMap<Long, Double>();
        HashMap<Long, Double> sensorReadingsOverTimeMapForSensorThree = new HashMap<Long, Double>();
        HashMap<Long, Double> sensorReadingsOverTimeMapForSensorFour = new HashMap<Long, Double>();


        while (rowItr.hasNext()) {
            List<FieldValue> columns = rowItr.next();
            long time = 0;
            for (int loopCount = 0; loopCount < columns.size(); loopCount++) {
                if (loopCount == 0) {
                    time = columns.get(loopCount).getLongValue();
                } else {
                    if (loopCount == 1) {
                        if (!sensorReadingsOverTimeMapForSensorOne.containsKey(time))
                            sensorReadingsOverTimeMapForSensorOne.put(time, columns.get(loopCount).getDoubleValue());
                    } else {
                        if (loopCount == 2) {
                            if (!sensorReadingsOverTimeMapForSensorTwo.containsKey(time))
                                sensorReadingsOverTimeMapForSensorTwo.put(time, columns.get(loopCount).getDoubleValue());
                        } else {
                            if (loopCount == 3) {
                                if (!sensorReadingsOverTimeMapForSensorThree.containsKey(time))
                                    sensorReadingsOverTimeMapForSensorThree.put(time, columns.get(loopCount).getDoubleValue());
                            } else {
                                if (loopCount == 4) {
                                    if (!sensorReadingsOverTimeMapForSensorFour.containsKey(time))
                                        sensorReadingsOverTimeMapForSensorFour.put(time, columns.get(loopCount).getDoubleValue());

                                } else {
                                    if (loopCount == 5) {
                                        if (!rowItr.hasNext())
                                            latestRulVal = columns.get(loopCount).getDoubleValue();
                                    }
                                }
                            }
                        }
                    }
                }

            }

        }

        sensorsHistoryMap.put("SensorMeasure2", sensorReadingsOverTimeMapForSensorOne);
        sensorsHistoryMap.put("SensorMeasure4", sensorReadingsOverTimeMapForSensorTwo);
        sensorsHistoryMap.put("SensorMeasure9", sensorReadingsOverTimeMapForSensorThree);
        sensorsHistoryMap.put("SensorMeasure11", sensorReadingsOverTimeMapForSensorFour);

        DeviceSensorReadingsOverTimeResponse deviceSensorReadingsOverTimeResponse = new DeviceSensorReadingsOverTimeResponse();

        deviceSensorReadingsOverTimeResponse.setDeviceSensorReadings(sensorsHistoryMap);
        deviceSensorReadingsOverTimeResponse.setLatestRulVal(latestRulVal);
        return deviceSensorReadingsOverTimeResponse;
    }

    private String fetchSensorReadingsForDeviceQuery(String industrialPlantId, String deviceId, String fromDate) {
        String sensorReadingsForDeviceQuery = "SELECT Cycle,SensorMeasure2,SensorMeasure4,SensorMeasure9,SensorMeasure11,RemainingOperationCycles FROM [" + tableName + "] where IndustrialPlantName like '" + industrialPlantId + "' and\n" +
                "UnitNumber like '" + deviceId + "'  and PredictedDate >  DATETIME(\"" + fromDate + "\")  order by Cycle";
        System.out.println(sensorReadingsForDeviceQuery);
        return sensorReadingsForDeviceQuery;
    }

    /**
     * The method is responsible for fetching devices that is being monitored
     * in the oilrig idenitfied by industrial plant Id from bigquery along
     * with its Remaining LifeCycle values.
     */

    public ArrayList<Device> getDevicesLifeCyclePredictions(String industrialPlantId, double latitude, double longtitude, int durationInMins) {
        //query bigquery table for the given oilrigId and get list of devices and its latest predictions
        ArrayList<Device> deviceList = new ArrayList<Device>();
        String deviceAndPredictionsQuery = fetchDeviceAndLatestPreditionsQuery(industrialPlantId, latitude, longtitude, getFromDate(durationInMins));
        Job deviceAndPredictionsJob = createJob(deviceAndPredictionsQuery, bigQueryClient);
        waitForJobCompletion(deviceAndPredictionsJob);
        QueryResponse response = bigQueryClient.getQueryResults(deviceAndPredictionsJob.getJobId());
        QueryResult result = processResponseAndGetResult(response);
        Iterator<List<FieldValue>> rowItr = result.iterateAll().iterator();

        while (rowItr.hasNext()) {
            List<FieldValue> columns = rowItr.next();
            Device device = new Device();

            for (int loopCount = 0; loopCount < columns.size(); loopCount++) {
                if (loopCount == 0) {
                    device.setName(columns.get(loopCount).getStringValue());
                } else {
                    if (loopCount == 1) {
                        device.setRulVal(columns.get(loopCount).getDoubleValue());
                    }
                }

            }
            deviceList.add(device);
        }

        return deviceList;
    }

    private String getFromDate(int durationInMins) {
        return LocalDateTime.now().minusMinutes(durationInMins).toString();
    }
}
