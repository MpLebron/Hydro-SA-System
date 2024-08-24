package com.opengms.sabackproject.service;

import com.opengms.sabackproject.dao.ComputableModelDao;
import com.opengms.sabackproject.entity.ComputableModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ComputableModelService {

    @Autowired
    ComputableModelDao computableModelDao;

    public List<ComputableModel> getAllModel(){

        List<ComputableModel> models = computableModelDao.findAll();

        return models;
    }

    public ComputableModel getModelByName(String name){
        ComputableModel model = computableModelDao.getFirstByName(name);
        return model;
    }

    public ComputableModel getByOid(String oid){
        ComputableModel model = computableModelDao.getFirstByOid(oid);
        return model;
    }
}
