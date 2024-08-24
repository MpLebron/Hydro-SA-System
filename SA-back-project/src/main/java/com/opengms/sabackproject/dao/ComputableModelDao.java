package com.opengms.sabackproject.dao;

import com.opengms.sabackproject.entity.ComputableModel;
import org.springframework.data.mongodb.repository.MongoRepository;


public interface ComputableModelDao extends MongoRepository<ComputableModel,String> {
    ComputableModel getFirstByName(String name);

    ComputableModel getFirstByOid(String oid);
}
