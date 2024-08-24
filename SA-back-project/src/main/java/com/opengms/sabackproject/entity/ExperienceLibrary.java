package com.opengms.sabackproject.entity;

import lombok.Data;
import org.springframework.data.annotation.Id;


@Data
public class ExperienceLibrary {
    @Id
    String id;
    String model;
    String originModel;
    String researchArea;

    String[] modelParams;
    String modelParamsRange;

    String saMethods;
    String objectiveFun;

    String simTimes;
    UploadFile[] saResults;

    String source;
    String sourceUrl;

    String geoJsonName;
    String geoJson;
}
