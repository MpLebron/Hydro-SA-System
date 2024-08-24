package com.opengms.sabackproject.dao;

import com.opengms.sabackproject.entity.SA_Project;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface ProjectDao extends MongoRepository<SA_Project,String> {
    SA_Project getByPid(String pid);
}
