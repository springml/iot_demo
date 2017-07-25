package com.springml.device.service.api;


import java.util.ArrayList;
import java.util.Arrays;

import com.google.gson.Gson;
import com.springml.device.service.model.OilRig;
import com.springml.device.service.model.OilRigsResponse;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.skyscreamer.jsonassert.JSONAssert;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.RequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.web.context.WebApplicationContext;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.setup.MockMvcBuilders.webAppContextSetup;

/**
 * Created by kaarthikraaj on 24/7/17.
 */
@RunWith(SpringRunner.class)
@SpringBootTest(classes = DeviceLifeCyclePredictionVisualsationApplication.class)

@WebAppConfiguration

public class DeviceLifeCyclePredictionVisualisationResourceTest {



        private MockMvc mockMvc;

        @Autowired
        private DeviceLifecyclePredictionVisualisationServer deviceLifecyclePredictionVisualisationServer;

        @Autowired
         private WebApplicationContext webApplicationContext;

        @Before
        public void setUp() {
            this.mockMvc = webAppContextSetup(webApplicationContext).build();
        }
        @Test

        public void getOilRigs() throws Exception {
            mockMvc.perform(get("/getOilRigs")
                    .contentType(MediaType.APPLICATION_JSON)
                    .param("durationInMins","75000"))
                    .andExpect(jsonPath("$.oilRigs").exists())
                    .andExpect(status().is2xxSuccessful());



        }
    @Test
    public void getSensorReadingsForDevice() throws Exception {
        mockMvc.perform(get("/getSensorReadingsForDevice")
                .contentType(MediaType.APPLICATION_JSON)
                .param("durationInMins","75000")
                .param("industrialPlantId","SAR-101")
                .param("deviceId","Unit0"))
                .andExpect(jsonPath("$.deviceSensorReadings").exists())
                .andExpect(status().is2xxSuccessful());



    }

    @Test
    public void getDeviceLifecyclePredictions() throws Exception {
        mockMvc.perform(get("/getDeviceLifecyclePredictions")
                .contentType(MediaType.APPLICATION_JSON)
                .param("durationInMins","75000")
                .param("oilRigId","SAR-101")
                .param("latitude","37.720427")
                .param("longtitude","-95.96803"))
                .andExpect(jsonPath("$.response").exists())
                .andExpect(status().is2xxSuccessful());



    }




}
