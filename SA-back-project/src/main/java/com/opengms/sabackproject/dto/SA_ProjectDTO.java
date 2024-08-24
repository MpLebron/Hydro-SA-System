package com.opengms.sabackproject.entity;

import com.alibaba.fastjson.JSONObject;
import lombok.Data;
import org.springframework.data.annotation.Id;

import java.util.ArrayList;
import java.util.List;

@Data
public class SA_ProjectDTO {
    @Id
    String id;
    // 项目ID
    String pid;
    String name;
    String description;
    // 模型ID
    String oid;
    String md5;
    String modelName;
    String modelDescription;

    // 待测参数
    List<SA_Param> paramList;

    // 模拟设置
    SimSetting simSetting;

    // 敏感性系数结果
    List<JSONObject> scoreSA;

    // 采样结果
    ArrayList<Float[]> paramsSet;

    // 模拟结果
    JSONObject simResult;

}
