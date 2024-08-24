package com.opengms.sabackproject.entity;

import com.alibaba.fastjson.JSONObject;
import lombok.Data;
import org.springframework.data.annotation.Id;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Data
public class SA_Project {
    @Id
    String id;
    // 项目ID
    String pid;
    String name;
    String description;
    Date createTime;
    // 模型ID
    String oid;
    String md5;
    String modelName;
    String modelDescription;

    // 数据和参数都在mdl里
    String mdl;
    JSONObject mdlJson;

    // 待测参数
    List<SA_Param> paramList;

    // 模拟设置
    SimSetting simSetting;

    Observed observed;
    String[] objectiveFun;

    // 采样结果
    ArrayList<Float[]> paramsSet;

    // 敏感性系数结果
    List<JSONObject> scoreSA;

    // 模拟结果
    JSONObject simResult;
    String[] labels;

    // 参数率定结果
    List<JSONObject> scoreObj;

    // 单次模拟参数

    // 单次模拟结果

}
