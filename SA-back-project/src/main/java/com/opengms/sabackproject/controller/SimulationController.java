package com.opengms.sabackproject.controller;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.opengms.sabackproject.bean.JsonResult;
import com.opengms.sabackproject.dao.ProjectDao;
import com.opengms.sabackproject.entity.*;
import com.opengms.sabackproject.entity.support.TaskData;
import com.opengms.sabackproject.service.ComputableModelService;
import com.opengms.sabackproject.service.ProjectService;
import com.opengms.sabackproject.service.SimulationService;
import com.opengms.sabackproject.utils.ResultUtils;
import com.opengms.sabackproject.utils.Utils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.UUID;


@RestController
@RequestMapping("/simulation")
public class SimulationController {


    @Autowired
    SimulationService simulationService;

    @Autowired
    ComputableModelService computableModelService;

    @Autowired
    ProjectService projectService;

    @RequestMapping(value = "/sample",method = RequestMethod.POST)
    public JsonResult parameterSample(@RequestParam("projectId") String projectId,
                                @RequestParam("params") String params,
                                @RequestParam("setting") String simSetting) throws IOException, InterruptedException {
        SA_Project project = projectService.getProjectByPid(projectId);

        List<SA_Param> paramList = JSON.parseArray(params,SA_Param.class);
        project.setParamList(paramList);

        SimSetting setting = JSON.parseObject(simSetting,SimSetting.class);

        project.setSimSetting(setting);

        // 存参数与配置
        String paramsFileName = simulationService.writeParamsAndSetting(project);
        // 参数采样
        boolean success = simulationService.parameterSample(paramsFileName);
        // 读取采样结果
        if(success){
            ArrayList<Float[]> paramsSet = simulationService.readSample(paramsFileName);
            project.setParamsSet(paramsSet);
            projectService.saveProject(project);
            return ResultUtils.success(paramsSet);
        }
        return ResultUtils.error(-2,"sample failed!");
    }

    @RequestMapping(value = "/invoke",method = RequestMethod.POST)
    public JsonResult invoke(@RequestBody JSONObject lists){ //HttpServletRequest request 暂时没有用户概念
        ComputableModel computableModel=computableModelService.getByOid(lists.getString("oid"));
        String mdlStr=computableModel.getMdl();
        JSONObject mdlJson= Utils.convertMdl(mdlStr);
        System.out.println(mdlJson);
        JSONObject mdl=mdlJson.getJSONObject("mdl");
        JSONArray states=mdl.getJSONArray("states");
        //截取RelatedDatasets字符串

        JSONArray outputs=new JSONArray();
        for(int i=0;i<states.size();i++){
            JSONObject state=states.getJSONObject(i);
            JSONArray events=state.getJSONArray("event");
            for(int j=0;j<events.size();j++){
                JSONObject event=events.getJSONObject(j);
                String eventType=event.getString("eventType");
                if(eventType.equals("noresponse")){
                    JSONObject output=new JSONObject();
                    output.put("statename",state.getString("name"));
                    output.put("event",event.getString("eventName"));
                    JSONObject template=new JSONObject();

                    JSONArray dataArr=event.getJSONArray("data");
                    if(dataArr!=null) {
                        JSONObject data = dataArr.getJSONObject(0);
                        String dataType = data.getString("dataType");
                        if (dataType.equals("external")) {
                            String externalId = data.getString("externalId");

                            template.put("type", "id");
                            template.put("value", externalId.toLowerCase());
                            output.put("template", template);

                        } else if (dataType.equals("internal")) {
                            JSONArray nodes = data.getJSONArray("nodes");
                            if (nodes != null) {
                                if(data.getString("schema")!=null) {
                                    template.put("type", "schema");
                                    template.put("value", data.getString("schema"));
                                    output.put("template", template);
                                }else{
                                    template.put("type", "none");
                                    template.put("value", "");
                                    output.put("template", template);
                                }
                            } else {
                                template.put("type", "none");
                                template.put("value", "");
                                output.put("template", template);
                            }
                        } else {
                            template.put("type", "none");
                            template.put("value", "");
                            output.put("template", template);
                        }
                    }else {
                        template.put("type", "none");
                        template.put("value", "");
                        output.put("template", template);
                    }
                    outputs.add(output);
                }
            }
        }
        lists.put("outputs",outputs);


//        lists.remove("oid");
        String username = "1565916523@qq.com";
        lists.put("userName", username);

        JSONObject result = simulationService.invoke(lists);
        if (result == null) {
            return ResultUtils.error(-2, "invoke failed!");
        }
        else {
            Task task = new Task();
            task.setOid(UUID.randomUUID().toString());
            task.setProjectId(lists.getString("projectId"));
            task.setNumber(lists.getInteger("number"));
            task.setComputableId(lists.getString("oid"));
            task.setComputableName(computableModel.getName());
            task.setTaskId(result.get("tid").toString());
            task.setIp(result.get("ip").toString());
            task.setPort((Integer)result.get("port"));
            task.setUserId(username);
            task.setIntegrate(false);
            task.setPermission("private");
            task.setRunTime(new Date());
            task.setStatus(0);
            JSONArray inputs = lists.getJSONArray("inputs");
            task.setInputs(JSONObject.parseArray(inputs.toJSONString(), TaskData.class));
            task.setOutputs(null);

            simulationService.save(task);

            return ResultUtils.success(result);
        }

    }

    @RequestMapping(value = "/single-sim-result", method = RequestMethod.POST)
    public JsonResult getSingleResult(@RequestBody JSONObject data) throws IOException, InterruptedException {
        JSONObject out=simulationService.getSingleTaskResult(data);
        return ResultUtils.success(out);
    }

    @RequestMapping(value = "/compute-sa",method = RequestMethod.GET)
    public JsonResult computeSA(String pid) throws IOException, InterruptedException {
        SA_Project project = projectService.getProjectByPid(pid);
        ///while (true){ // 这会导致前端等待超时
            if (simulationService.checkExtract(project)){   // 当所有结果都写入文件中才可以计算
                List<JSONObject> scoreSA = simulationService.computeSA(project);
                if(scoreSA == null){
                    return ResultUtils.error(-2,"SA计算失败");
                }else{
                    project.setScoreSA(scoreSA);
                    projectService.saveProject(project);
                    return ResultUtils.success(scoreSA);
                }
            }else{
                return ResultUtils.success("waiting");
            }
        //}
    }

    @RequestMapping(value = "/sim-result",method = RequestMethod.GET)
    public JsonResult getSimResult(String pid) throws IOException {
        SA_Project project = projectService.getProjectByPid(pid);
        if (simulationService.checkExtract(project)){
            JSONObject simResult = simulationService.getSimResult(project);
            if(simResult == null){
                return ResultUtils.error(-2,"获取模拟结果失败");
            }else{
                project.setSimResult(simResult);
                projectService.saveProject(project);
                return ResultUtils.success(simResult);
            }
        }else{
            return ResultUtils.success("waiting");
        }

    }

    @RequestMapping(value = "/labels",method = RequestMethod.GET)
    public JsonResult getLabels(String pid) throws IOException{
        String[] labels = simulationService.getLabels(pid);
        if(labels == null){
            return ResultUtils.error(-2,"获取X轴labels失败");
        }else{
            SA_Project project = projectService.getProjectByPid(pid);
            project.setLabels(labels);
            projectService.saveProject(project);
            return ResultUtils.success(labels);
        }
    }

    @RequestMapping(value = "/compute-obj-for-sa", method = RequestMethod.GET)
    JsonResult computeObjForSA(String pid, String targetsStr, String urlsStr) throws IOException, InterruptedException {
        SA_Project project = projectService.getProjectByPid(pid);
        String[] targets = targetsStr.split(",");
        String[] urls = urlsStr.split(",");
        if(simulationService.checkExtract(project)){    // 当所有结果都写入文件中才可以计算
            List<JSONObject> scoreObjList = new ArrayList<>();
            for (int i = 0; i < targets.length; i++) {
                JSONObject scoreObj = simulationService.computeObj(pid, targets[i], urls[i]);
                if(scoreObj == null){
                    return ResultUtils.error(-2,"目标函数计算失败");
                }else{
                    scoreObjList.add(scoreObj);
                }
            }
            project.setScoreObj(scoreObjList);
            projectService.saveProject(project);
            return ResultUtils.success(scoreObjList);
        }else{
            return ResultUtils.success("waiting");
        }
    }

    @RequestMapping(value = "/clear-sa-sim-result",method = RequestMethod.DELETE)
    public JsonResult clearSASimResult(String pid){
        simulationService.clearSASimResult(pid);
        return ResultUtils.success();
    }
}
