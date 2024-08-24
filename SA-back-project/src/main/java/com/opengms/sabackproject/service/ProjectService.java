package com.opengms.sabackproject.service;

import com.opengms.sabackproject.dao.ProjectDao;
import com.opengms.sabackproject.entity.SA_Project;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProjectService {

    @Autowired
    ProjectDao projectDao;
    public void saveProject(SA_Project project) {
        projectDao.save(project);
    }

    public SA_Project getProjectByPid(String pid) {
        return projectDao.getByPid(pid);
    }

    public List<SA_Project> getAll(){
        return projectDao.findAll();
    }
}
