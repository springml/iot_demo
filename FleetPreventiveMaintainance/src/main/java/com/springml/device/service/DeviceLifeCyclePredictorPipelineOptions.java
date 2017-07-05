package com.springml.device.service;

import com.google.cloud.dataflow.sdk.options.DataflowPipelineOptions;
import com.google.cloud.dataflow.sdk.options.Default;
import com.google.cloud.dataflow.sdk.options.Description;
import com.google.cloud.dataflow.sdk.options.Validation;


public interface DeviceLifeCyclePredictorPipelineOptions extends DataflowPipelineOptions {

    @Description("ProjectId where data source topic lives")
    @Default.String("mlpdm-168115")
    @Validation.Required
    String getSourceProject();

    void setSourceProject(String value);

    @Description("TopicId of source topic")
    @Default.String("hemanth_iot_test")
    @Validation.Required
    String getSourceTopic();

    void setSourceTopic(String value);

    @Description("subscription")
    @Default.String("IOT")
    @Validation.Required
    String getSubscriptionName();

    void setSubscriptionName(String value);

    @Description("Fleet Preventive Maintance ML url")
    @Default.String("https://ml.googleapis.com/v1beta1/projects/mlpdm-168115/models/predictivemaintenance_v5/versions/v5:predict")
    @Validation.Required
    String getFleetPreventMLUrl();

    void setFleetPreventMLUrl(String value);

    @Description("Fleet Preventive Maintance ML API Key")
    @Default.String("testAPIKey")
    @Validation.Required
    String getApiKey();

    void setApiKey(String value);

    @Description("Fleet Preventive Maintance Device Sensor readings Table")
    @Default.String("mlpdm-168115:FleetMaintainance.DeviceSensorReadings")
    @Validation.Required
    String getDeviceSensorReadingsTable();

    void setDeviceSensorReadingsTable(String value);

    @Description("Fleet Preventive Maintance Device Remaining lifecycle Table")
    @Default.String("mlpdm-168115:FleetMaintainance.DeviceRemainingOperationCycles")
    @Validation.Required
    String getDeviceRemainingLifeCycleOperationsTable();

    void setDeviceRemainingLifeCycleOperationsTable(String value);
}