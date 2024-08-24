package com.opengms.sabackproject.entity;

import com.opengms.sabackproject.entity.support.TaskData;
import lombok.Data;
import org.springframework.data.annotation.Id;

import java.util.Date;
import java.util.List;

@Data
public class Task {
    @Id
    String id;
    String oid;
    String projectId;
    String taskId;
    int number;
    String computableId;
    String computableName;
    String userId;
    String description;
    String ip;
    int port;
    int loadTime;

    Date runTime;

    int status;//Started: 1, Finished: 2, Inited: 0, Error: -1

    //    List<String> isPublic;//public ;noPublic ;userNames; public和noPublic都放数组头
    String permission;
    List<TaskData> inputs;
    List<TaskData> outputs;

    Boolean integrate;
}
