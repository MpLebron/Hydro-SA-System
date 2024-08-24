package com.opengms.sabackproject.entity;

import lombok.Data;
import org.bson.types.Binary;
import org.springframework.data.annotation.Id;

import java.time.LocalDateTime;

@Data
public class UploadFile {
    @Id
    String id;
    /** 文件名 */
    String name;
    /** 上传时间 */
    LocalDateTime createdTime;
    /** 文件内容 */
    Binary content;
    /** 文件类型 */
    String contentType;
    /** 文件大小 */
    long size;
}
