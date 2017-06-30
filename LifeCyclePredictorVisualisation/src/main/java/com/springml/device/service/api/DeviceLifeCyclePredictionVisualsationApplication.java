package com.springml.device.service.api;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

/**
 * Spring Boot application's main class
 *
 */
@Configuration
@SpringBootApplication
public class DeviceLifeCyclePredictionVisualsationApplication {
    public static void main(String args[]) {
        SpringApplication.run(DeviceLifeCyclePredictionVisualsationApplication.class, args);
    }

    @Bean
    public DeviceLifecyclePredictionVisualisationServer deviceLifecyclePredictionVisualisationServer() {
        return new DeviceLifecyclePredictionVisualisationServer();
    }


    @Bean
    public OilRigsDevicesManager oilRigsDevicesManager() {
        return new OilRigsDevicesManager();
    }

    public FilterRegistrationBean corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true);
        config.addAllowedOrigin("*");
        config.addAllowedHeader("*");
        config.addAllowedMethod("*");
        source.registerCorsConfiguration("/**", config);
        FilterRegistrationBean bean = new FilterRegistrationBean(new CorsFilter(source));
        bean.setOrder(0);
        return bean;
    }


}
