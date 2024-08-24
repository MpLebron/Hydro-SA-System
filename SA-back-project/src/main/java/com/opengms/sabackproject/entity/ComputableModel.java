package com.opengms.sabackproject.entity;

import com.alibaba.fastjson.JSONObject;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class ComputableModel {
    @Id
    String id;
    String oid;
    String originModel;
    String name;
    String description;

    String md5;
    String mdl;
    JSONObject mdlJson;


    // 等等
}
