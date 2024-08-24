package com.opengms.sabackproject.entity;

import lombok.Data;


@Data
public class SimSetting {
    String saMethod;
    String sampleMethod;
//    String methodName;
    int simTimes;
    String[] simTargets;
    String[] observations;
    String[] objectiveFuns;
}
