package com.springml.device.service;

import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.*;
import com.google.api.client.http.json.JsonHttpContent;
import com.google.gson.Gson;
import com.springml.device.service.model.LifeCyclePredictionResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.ByteArrayOutputStream;
import java.io.Serializable;
import java.util.Collections;

/**
 * This the the DeviceLifeCyclePredictor API Client that  is responsible for calling
 * ML API and parsing the response
 */
public class DeviceLifeCyclePredictorClient implements Serializable {
    private static final Logger LOG = LoggerFactory.getLogger(DeviceLifeCyclePredictorClient.class);
    private String CLOUDML_SCOPE = "https://www.googleapis.com/auth/cloud-platform";

    /*
        The method is responsible for calling ML API
         */
    public LifeCyclePredictionResponse getPredictedLifeCycle(JsonHttpContent jsonHttpContent, String predictRestUrl) {
        LifeCyclePredictionResponse predictionResponse = new LifeCyclePredictionResponse();

        try {
            GoogleCredential credential = GoogleCredential.getApplicationDefault()
                    .createScoped(Collections.singleton(CLOUDML_SCOPE));
            HttpTransport httpTransport = GoogleNetHttpTransport.newTrustedTransport();
            HttpRequestFactory requestFactory = httpTransport.createRequestFactory(
                    credential);
            GenericUrl url = new GenericUrl(predictRestUrl);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            jsonHttpContent.writeTo(baos);
            LOG.info("The ML URL being tried is " + predictRestUrl);
            LOG.info("Executing CloudML predictions with payload : " + baos.toString());
            HttpRequest request = requestFactory.buildPostRequest(url, jsonHttpContent);

            HttpResponse response = request.execute();
            Gson gson = new Gson();
            predictionResponse = gson.fromJson(response.parseAsString(), LifeCyclePredictionResponse.class);

            LOG.info("CloudML prediction response \n" + predictionResponse);
        } catch (Exception e) {
            LOG.error("Error while getting predictions using CloudML", e);
        }

        return predictionResponse;
    }


}
