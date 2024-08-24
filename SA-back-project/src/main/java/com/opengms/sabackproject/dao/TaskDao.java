package com.opengms.sabackproject.dao;

import com.opengms.sabackproject.entity.Task;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface TaskDao extends MongoRepository<Task,String> {
    Task findFirstByTaskId(String tid);
    List<Task> findAllByProjectId(String pid);
}
