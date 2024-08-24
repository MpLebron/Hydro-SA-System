package com.opengms.sabackproject.entity;

import lombok.Data;

@Data
public class SA_Param {
    String name;
    String description;
    String changeType;
    Float left;
    Float right;
    Float value;
}
