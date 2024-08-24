package com.opengms.sabackproject.controller;

import com.opengms.sabackproject.bean.JsonResult;
import com.opengms.sabackproject.entity.ComputableModel;
import com.opengms.sabackproject.entity.SA_Project;
import com.opengms.sabackproject.service.ComputableModelService;
import com.opengms.sabackproject.service.ProjectService;
import com.opengms.sabackproject.utils.ResultUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/project")
public class ProjectController {

    SimpleDateFormat sdf = new SimpleDateFormat("/yyyy/MM/dd/");

    @Autowired
    ComputableModelService computableModelService;
    @Autowired
    ProjectService projectService;

    @RequestMapping(value = "/create",method = RequestMethod.POST)
    public JsonResult CreateNewProject(@RequestBody SA_Project project){

        project.setPid(UUID.randomUUID().toString());
        project.setCreateTime(new Date());
        // 查找模型信息
        String oid = project.getOid();
        ComputableModel model = computableModelService.getByOid(oid);

        // 设置本次项目的模型信息
        project.setMd5(model.getMd5());
        project.setModelName(model.getName());
        project.setModelDescription(model.getDescription());
        project.setMdl(model.getMdl());
        project.setMdlJson(model.getMdlJson());

        projectService.saveProject(project);
        return ResultUtils.success(project.getPid());
    }

    @RequestMapping(value = "/getByPid",method = RequestMethod.GET)
    public JsonResult getByPid(String pid){
        SA_Project project = projectService.getProjectByPid(pid);
        return ResultUtils.success(project);
    }

    @RequestMapping(value = "/getAllProjects", method = RequestMethod.GET)
    public JsonResult getAllProjects(){
        // 此处应该返回SA_Project的简约版DTO，不应把每一个字段都传回前端
        List<SA_Project> list = projectService.getAll();
        // 剔除信息不完整的项目
        List<SA_Project> newList = new ArrayList<>();
        for (int i = 0; i < list.size(); i++) {
            SA_Project project = list.get(i);
            if (project.getScoreSA() != null){
                newList.add(project);
            }
        }
        return ResultUtils.success(newList);
    }
}
