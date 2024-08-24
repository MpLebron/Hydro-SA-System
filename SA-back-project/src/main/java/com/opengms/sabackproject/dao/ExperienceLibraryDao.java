package com.opengms.sabackproject.dao;

import com.opengms.sabackproject.entity.ExperienceLibrary;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface ExperienceLibraryDao extends MongoRepository<ExperienceLibrary, String> {
    ExperienceLibrary[] getAllByModel(String model);
}
