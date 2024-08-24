package com.opengms.sabackproject.dao;

import com.opengms.sabackproject.entity.Task;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface SimulationDao extends MongoRepository<Task,String> {
}
