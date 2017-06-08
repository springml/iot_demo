package com.springml.device.service;

import com.google.api.services.bigquery.model.TableFieldSchema;
import com.google.api.services.bigquery.model.TableRow;
import com.google.api.services.bigquery.model.TableSchema;
import com.google.cloud.dataflow.sdk.Pipeline;
import com.google.cloud.dataflow.sdk.coders.TableRowJsonCoder;
import com.google.cloud.dataflow.sdk.io.BigQueryIO;
import com.google.cloud.dataflow.sdk.io.PubsubIO;
import com.google.cloud.dataflow.sdk.options.PipelineOptionsFactory;
import com.google.cloud.dataflow.sdk.transforms.ParDo;
import com.google.cloud.dataflow.sdk.values.PCollection;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by kaarthikraaj on 2/6/17.
 */
public class DeviceServiceGDF {

    public static void main(String args[]) {
        DeviceLifeCyclePredictorPipelineOptions options =
                PipelineOptionsFactory.fromArgs(args).withValidation().as(DeviceLifeCyclePredictorPipelineOptions.class);
        Pipeline p = Pipeline.create(options);
        System.out.println("Project is" + options.getSourceProject() + " subscription" + options.getSubscriptionName());
        PCollection<TableRow> datastream = p.apply(PubsubIO.Read.named("Read device iot data from PubSub")
                // .subscription(String.format("projects/%s/subscriptions/%s", options.getSourceProject(), options.getSubscriptionName()))
                .topic(String.format("projects/%s/topics/%s", options.getSourceProject(), options.getSourceTopic()))
                .timestampLabel("ts")
                .withCoder(TableRowJsonCoder.of()));

        String fleetPreventMLServiceUrl = options.getFleetPreventMLUrl();
        //String apiKey = options.getApiKey();
        // String redeemCouponServiceUrl = options.getRedeemCouponServiceUrl();
        datastream.apply(BigQueryIO.Write.named("Write to BigQuery")
                .withCreateDisposition(BigQueryIO.Write.CreateDisposition.CREATE_IF_NEEDED)
                .withSchema(getDeviceSensorReadingsSchema())
                .withWriteDisposition(BigQueryIO.Write.WriteDisposition.WRITE_APPEND)
                .to(options.getDeviceSensorReadingsTable()));
        datastream.apply("Invoking FleetPreventiveMaintainanceML", ParDo.of(new DeviceLifeCyclePredictorMLTransormation(fleetPreventMLServiceUrl)))
                .apply(BigQueryIO.Write.named("Write remaining lifecycle predictions response to BigQuery")
                        .withCreateDisposition(BigQueryIO.Write.CreateDisposition.CREATE_IF_NEEDED)
                        .withSchema(getDeviceRemainngLifeCyleSchema())
                        .withWriteDisposition(BigQueryIO.Write.WriteDisposition.WRITE_APPEND)
                        .to(options.getDeviceRemainingLifeCycleOperationsTable()));
               /* .apply("Invoking Redeem Coupon Service",ParDo.of(new RedeemCouponServiceClient(redeemCouponServiceUrl,apiKey)))
                ;
                        */

        p.run();
    }

    private static TableSchema getDeviceRemainngLifeCyleSchema() {
        List<TableFieldSchema> fields = new ArrayList<>();

        fields.add(new TableFieldSchema().setName("Unit_Number").setType("INTEGER"));
        fields.add(new TableFieldSchema().setName("RemainingOperationCycles").setType("FLOAT"));
        return new TableSchema().setFields(fields);
    }

    private static TableSchema getDeviceSensorReadingsSchema() {
        List<TableFieldSchema> fields = new ArrayList<>();
        fields.add(new TableFieldSchema().setName("UnitNumber").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("Cycle").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure19").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure18").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure17").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure16").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure15").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure14").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure13").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure12").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure11").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure10").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure9").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure8").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure7").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure6").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure5").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure4").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure3").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure2").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure1").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure20").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("SensorMeasure21").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("OpSet3").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("OpSet2").setType("FLOAT"));
        fields.add(new TableFieldSchema().setName("OpSet1").setType("FLOAT"));
        return new TableSchema().setFields(fields);
    }
}
