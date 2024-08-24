package com.opengms.sabackproject.service;

import ch.qos.logback.core.util.FileUtil;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.opengms.sabackproject.dao.SimulationDao;
import com.opengms.sabackproject.dao.TaskDao;
import com.opengms.sabackproject.entity.*;
import com.opengms.sabackproject.entity.support.TaskData;
import com.opengms.sabackproject.utils.Utils;
import org.apache.commons.lang.StringUtils;
import org.apache.tomcat.util.http.fileupload.FileUtils;
import org.bson.types.Binary;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import org.springframework.util.ClassUtils;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.mock.web.MockMultipartFile;

import java.io.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static com.opengms.sabackproject.utils.Utils.convertMdl;
import static com.opengms.sabackproject.utils.Utils.postJSON;

@Service
public class SimulationService {

    @Value("${resourcePath}")
    private String resourcePath;

    @Value("${managerServerIpAndPort}")
    private String managerServerIpAndPort;

    @Autowired
    public SimulationDao simulationDao;

    @Autowired
    public TaskDao taskDao;

    @Autowired
    public ComputableModelService computableModelService;

    /**
     * 保存参数与配置文件 项目ID作为文件路径前缀
     */
    public String writeParamsAndSetting(SA_Project project) throws IOException {
        List<SA_Param> paramList = project.getParamList();
        SimSetting setting = project.getSimSetting();
        // 写文件
        String pid = project.getPid();
        // paramsSum.txt
        String paramsFileName = resourcePath + "/" + pid +  "paramsSum.txt";
        File file = new File(paramsFileName);
        if(!file.exists()){
            file.createNewFile();
        }
        FileWriter writer = new FileWriter(paramsFileName);
        for (int i = 0; i < paramList.size(); i++) {
            SA_Param param = paramList.get(i);
            String line = param.getName() + ":" + param.getLeft() + "," + param.getRight()+"\n";
            writer.write(line);
        }
        writer.close();
        // simSetting.txt
        String settingFileName = resourcePath + "/" + pid + "simSetting.txt";
        file = new File(settingFileName);
        if(!file.exists()){
            file.createNewFile();
        }
        writer = new FileWriter(settingFileName);
        String targets = StringUtils.join(setting.getSimTargets(),",");
        String observations = StringUtils.join(setting.getObservations(),",");
        String objectiveFuns = StringUtils.join(setting.getObjectiveFuns(),",");
        writer.write("sampleMethod:"+setting.getSampleMethod()+"\n"+
                "SAmethod:"+setting.getSaMethod()+"\n"+
                "simTimes:"+setting.getSimTimes()+"\n"+
                "simTargets:"+targets+"\n"+
                "observations:"+observations+"\n"+
                "objectiveFuns:"+objectiveFuns);// 这四个是所有模型所共有的设置，其余设置需要在封装代码里自定义写入
        writer.close();
        return resourcePath + "/" + pid;
    }

    /**
     * 参数采样 脚本命令行参数：文件路径前缀
     * 脚本运行结果为 params_sampling文件
     */
    public boolean parameterSample(String paramsFileName) throws IOException, InterruptedException {
        String path = ClassUtils.getDefaultClassLoader().getResource("").getPath();
        String samplePath = path.substring(1) + "static/myResources/params_sampling.py";
        String cmd = "python " + samplePath + " " + paramsFileName;
        Process proc = Runtime.getRuntime().exec(cmd);

        int re = proc.waitFor();
        if (re == 0)
            return true;
        else
            return false;
    }

    public ArrayList<Float[]> readSample(String paramsFileName) throws IOException {
        String filePath = paramsFileName + "params_sampling.csv";
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "utf-8"));
        reader.readLine();//显示标题行,没有则注释掉
        String line = null;
        ArrayList<Float[]> paramsSet = new ArrayList<>();
        while((line=reader.readLine())!=null){
            String item[] = line.split(",");
            Float params[] = new Float[item.length];
            for (int i = 0; i < item.length; i++) {
                params[i] = Float.parseFloat(item[i]);
            }
            paramsSet.add(params);
        }
        return paramsSet;
    }

    /**
     * zhsh
     * 2020.12.07
     * 提交敏感性分析计算任务
     * 与直接/invoke不同的是，无法指定ip，port
     * 与直接/runTask不同的是，input，output都已经组织好，TaskSubmitDTO
     * 可以直接复用/submitTask接口
     */
    public JSONObject invoke(JSONObject lists) {

        JSONObject result = Utils.postJSON("http://" + managerServerIpAndPort + "/GeoModeling/computableModel/submitTask", lists);

        if (result != null) {
            if (result.getInteger("code") == 1) {
                return result.getJSONObject("data");
            }
        }

        return null;
    }

    public String save(Task task) {

        simulationDao.save(task);
        return "suc";
    }

    public Task findByTaskId(String taskId) {
        return taskDao.findFirstByTaskId(taskId);
    }

    // 为task output匹配templateId
    public Task templateMatch(Task task){

        String modelId = task.getComputableId();
        ComputableModel modelInfo = computableModelService.getByOid(modelId);
        JSONObject mdlInfo = convertMdl(modelInfo.getMdl());
        JSONObject mdlObj = mdlInfo.getJSONObject("mdl");
        JSONArray states = mdlObj.getJSONArray("states");

        List<TaskData> outputs = task.getOutputs();

        for (int i=0;i<states.size();i++){
            JSONObject obj = (JSONObject)states.get(i);
            JSONArray event = obj.getJSONArray("event");
            for( int j=0; j<event.size();j++ ){
                JSONObject file = (JSONObject) event.get(j);
                JSONArray dataArray = file.getJSONArray("data");
                JSONObject data = (JSONObject) dataArray.get(0);

                if(file.getString("eventType").equals("noresponse")){
                    for (TaskData output : outputs){
                        if(output.getEvent().equals(file.getString("eventName"))){
                            if(data.getString("dataType").equals("external"))
                                output.setTemplateId(data.getString("externalId"));
                            else
                                output.setTemplateId("schema");
                        }
                    }
                }
            }
        }
        task.setOutputs(outputs);
        return task;
    }

    /**
     * 提取每次模拟结果 脚本命令行参数为：eventName url eventName url ...
     * 脚本运行结果为 resultIndex resultForSA [resultForDisplay]
     */
    public boolean extractSingleResult(Task task) throws IOException {
        List<TaskData> outputs = task.getOutputs();

        String path = ClassUtils.getDefaultClassLoader().getResource("").getPath();
        String extract = path.substring(1) + "static/myResources/extract_result_" + task.getComputableName() +".py";
        String fileName = resourcePath + "/" + task.getProjectId();
        String cmd = "python " + extract + " " + fileName;

        String str = "";
        for (int i = 0; i < outputs.size(); i++) {
            TaskData state = outputs.get(i);
            str += " "+ state.getEvent() + " " + state.getUrl() ;
        }
        cmd += str;
        // 记录计算任务的顺序
        cmd += " " + task.getNumber();

        Process proc = Runtime.getRuntime().exec(cmd);

        return true;
//        不要等待，因为前端在等回复，不然前端容易阻塞，这造成的问题是计算SA时，每一次的结果不一定提取完成
//        int re = proc.waitFor();
//        if (re == 0)
//            return true;
//        else
//            return false;
    }

    public JSONObject getSingleTaskResult(JSONObject data) throws IOException {
        JSONObject out = new JSONObject();

        JSONObject result = Utils.postJSON("http://" + managerServerIpAndPort + "/GeoModeling/computableModel/refreshTaskRecord", data);

        ////update model status to Started, Started: 1, Finished: 2, Inited: 0, Error: -1
        Task task = findByTaskId(data.getString("tid"));
        int state = task.getStatus();
        int remoteState = result.getJSONObject("data").getInteger("status");
        if (remoteState != state) {
            task.setStatus(remoteState);
        }
        if (remoteState == 2) {
            boolean hasValue = false;
            JSONArray outputs = result.getJSONObject("data").getJSONArray("outputs");
            for (int i = 0; i < outputs.size(); i++) {
                if (!outputs.getJSONObject(i).getString("url").equals("")) {
                    hasValue = true;
                    break;
                }
            }
            if (!hasValue) {
                task.setStatus(-1);
            }
            for (int i = 0; i < outputs.size(); i++) {
                if (outputs.getJSONObject(i).getString("url").contains("[")) {//说明是单event多输出的情况
                    outputs.getJSONObject(i).put("multiple",true);
                }
            }

            task.setOutputs(result.getJSONObject("data").getJSONArray("outputs").toJavaList(TaskData.class));

            task = templateMatch(task);
        }
        save(task);


        if (task.getStatus() == 0) {
            out.put("status", 0);
        } else if (task.getStatus() == 1) {
            out.put("status", 1);
        } else if (task.getStatus() == 2) {
            out.put("status", 2);
            out.put("outputdata", task.getOutputs());
            boolean flag = extractSingleResult(task);
            System.out.println(flag);
        } else {
            // 模型执行出错
            out.put("status", -1);
        }
        return out;
    }

    public boolean checkExtract(SA_Project project) throws IOException {
        String totalPath = resourcePath + "/" + project.getPid() +  "res_total_output.dat";
        File file = new File(totalPath);
        if(!file.exists()) return false; // 如果不存在直接返回false
        BufferedReader reader = new BufferedReader(new FileReader(file));
        int line = 0;
        while (reader.readLine() != null) {
            line++;
        }
        reader.close();
        if (line >= project.getParamsSet().size())
            return true;
        else
            return false;
    }

    /**
     * 计算敏感性指标 命令行参数为：文件路径前缀
     */
    public List<JSONObject> computeSA(SA_Project project) throws IOException, InterruptedException {
        List<JSONObject> scoreSA = new ArrayList<>();
        // 获取项目资源路径，项目部署时这里可能会有问题
        String path = ClassUtils.getDefaultClassLoader().getResource("").getPath();

        String saScript = path.substring(1) + "static/myResources/SA_compute.py";
        String fileName = resourcePath + "/" + project.getPid() ;

        String cmd = "python " + saScript + " " + fileName;
        Process proc = Runtime.getRuntime().exec(cmd);

        int re = proc.waitFor();
        if (re == 0){
            scoreSA = getScoreSA(project);
            return scoreSA;
        }else
            return null;
    }

    public List<JSONObject> getScoreSA(SA_Project project) throws IOException {
        List<JSONObject> scoreSA = new ArrayList<>();
        String method = project.getSimSetting().getSaMethod();

        // 从Observation-State中获取所有target
        List<String> targets = getTargets(project);
        // 读取各个target的SA结果
        String fileName = resourcePath + "/" + project.getPid() ;
        for (int i = 0; i < targets.size(); i++) {
            JSONObject target = new JSONObject();
            target.put("target",targets.get(i));

//            String filePath = fileName + "SA_score_" + targets.get(i) + ".txt";
//            BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "utf-8"));

            // 读取SA结果文本只为展示，具体可视化效果通过绘制的图来展示
            String fileTxtPath = fileName + "SA_score_" + targets.get(i) + ".txt";
            File fileTXT = new File(fileTxtPath);
            Long filelength = fileTXT.length();
            byte[] filecontent = new byte[filelength.intValue()];
            FileInputStream in = new FileInputStream(fileTXT);
            in.read(filecontent);
            in.close();
            String scoreTXT = new String(filecontent, "UTF-8");
            // 结果图
            String fileFigurePath = fileName + "SA_score_figure_" + targets.get(i) + ".jpg";
            File fileFigure = new File(fileFigurePath);
            MultipartFile mulFile = new MockMultipartFile(
                    fileFigure.getName(),
                    fileFigure.getName(),
                    "jpg",
                    new FileInputStream(fileFigure)
            );
            UploadFile uploadFile = new UploadFile();
            uploadFile.setName(mulFile.getName());
            uploadFile.setCreatedTime(LocalDateTime.now());
            uploadFile.setContent(new Binary(mulFile.getBytes()));
            uploadFile.setContentType(mulFile.getContentType());
            uploadFile.setSize(mulFile.getSize());
            target.put("score", scoreTXT);
            target.put("figure", uploadFile);

//
//            String[] names = reader.readLine().split(",");
//            String[] params = new String[names.length-1];
//            for (int j = 0; j < params.length; j++) {
//                params[j] = names[j+1];
//            }
//            target.put("params",params);
//            String line = null;
//            for (int k = 0; k < 2; k++) {
//                line=reader.readLine();
//                String item[] = line.split(",");
//                Float values[] = new Float[item.length-1];
//                for (int j = 0; j < values.length; j++) {
//                    if(item[j+1].equals("nan")){
//                        values[j] = (float)0;
//                        continue;
//                    }
//                    values[j] = Float.parseFloat(item[j+1]);
//                }
//                target.put(item[0], values);
//            }
//            if(method.equals("sobol")){
//                List<Float[]> s2 = new ArrayList<>();
//                line=reader.readLine();
//                String item[] = line.split(",");
//                Float values[] = new Float[item.length-1];
//                for (int j = 0; j < values.length; j++) {
//                    if(item[j+1].equals("nan")){
//                        values[j] = (float)0;
//                        continue;
//                    }
//                    values[j] = Float.parseFloat(item[j+1]);
//                }
//                s2.add(values);
//                for (int j = 1; j < params.length; j++) {
//                    line=reader.readLine();
//                    item = line.split(",");
//                    values = new Float[item.length-1];
//                    for (int k = 0; k < values.length; k++) {
//                        if(item[k+1].equals("nan")){
//                            values[k] = (float)0;
//                            continue;
//                        }
//                        values[k] = Float.parseFloat(item[k+1]);
//                    }
//                    s2.add(values);
//                }
//                target.put("S2", values);
//            }

            scoreSA.add(target);
        }
        return scoreSA;
    }

    // 从Observation-State中获取所有target
    public List<String> getTargets(SA_Project project){
        List<String> targets = new ArrayList<>();
        JSONArray states = project.getMdlJson().getJSONObject("mdl").getJSONArray("states");
        for (int i = 0; i < states.size(); i++) {
            JSONObject state = states.getJSONObject(i);
            if(state.getString("name").equals("Observation")){
                JSONArray events = state.getJSONArray("event");
                for (int j = 0; j < events.size(); j++) {
                    targets.add(events.getJSONObject(j).getString("eventName"));
                }
            }
        }
        return targets;
    }
    /**
     * 获取所有模拟结果
     */
    public JSONObject getSimResult(SA_Project project) throws IOException {
        List<JSONObject> simResult = new ArrayList<>();
        // 从Observation-State中获取所有target
        List<String> targets = getTargets(project);
        // 读取各个target的模拟结果
        String fileName = resourcePath + "/" + project.getPid() ;
        for (int i = 0; i < targets.size(); i++) {
            JSONObject result = new JSONObject();
            result.put("target",targets.get(i));

            String filePath = fileName + "sim_result_" + targets.get(i) + ".dat";
            BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "utf-8"));
            String line = null;
            List<Float[]> allValues = new ArrayList<>();
            while((line=reader.readLine())!=null){
                String item[] = line.split(" ");
                Float values[] = new Float[item.length];
                for (int j = 0; j < item.length; j++) {
                    values[j] = Float.parseFloat(item[j]);
                }
                allValues.add(values);
            }
            result.put("allValues",allValues);
            simResult.add(result);
        }

        // 读取总的模拟结果，用于定性查看参数敏感性
        // 读取各个target的序号
        List<Float[]> totalResult = new ArrayList<>();
        String indexPath = fileName + "resultIndex.txt";
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(indexPath), "utf-8"));
        String line = null;
        List<Integer> resultIndex = new ArrayList<>();
        while((line=reader.readLine())!=null){
            String item[] = line.split(":");
            if(item[0].equals("resultIndexs")){
                String index[] = item[1].split(",");
                for (int i = 0; i < index.length; i++) {
                    resultIndex.add(Integer.parseInt(index[i]));
                }
            }
        }
        // 读取总的模拟结果
        String totalPath = fileName + "res_total_output.dat";
        for (int i = 0; i < resultIndex.size(); i++) {
            reader = new BufferedReader(new InputStreamReader(new FileInputStream(totalPath), "utf-8"));
            line = null;
            List<Float> values = new ArrayList<>();
            while((line=reader.readLine())!=null){
                String item[] = line.split(" ");
                values.add(Float.parseFloat(item[resultIndex.get(i)]));
            }
            Float[] vals = new Float[values.size()];
            values.toArray(vals);
            totalResult.add(vals);
        }

        JSONObject result = new JSONObject();
        result.put("simResult",simResult);
        result.put("totalResult",totalResult);
        return result;
    }

    /**
     * 获取X轴labels
     */
    public String[] getLabels(String pid) throws IOException {

        String filePath = resourcePath + "/" + pid +"labels.dat";
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "utf-8"));
        // 只有一行
        String line = reader.readLine();

        if(line != null){
            String[] labels = line.split(" ");
            return labels;
        }
        return null;
    }

    /**
     * 计算目标函数
     */
    public JSONObject computeObj(String pid, String eventName, String url) throws IOException, InterruptedException {
        JSONObject scoreObj = new JSONObject();

        // 调用python脚本计算目标函数得分
        Utils.downLoadFromUrl(url,pid+"obs_"+eventName+".txt",resourcePath);
        // 获取项目资源路径，项目部署时这里可能会有问题
        String path = ClassUtils.getDefaultClassLoader().getResource("").getPath();
        String objScript = path.substring(1) + "static/myResources/Obj_compute.py";
        String fileName = resourcePath + "/" + pid ;
        String cmd = "python " + objScript + " " + fileName + " " + eventName;
        Process proc = Runtime.getRuntime().exec(cmd);

        int re = proc.waitFor();
        if (re == 0)
            scoreObj = getScoreObj(pid, eventName);
        else
            return null;

        return scoreObj;
    }

    public JSONObject getScoreObj(String pid, String eventName) throws IOException {
        // 读取目标函数得分文件
        JSONObject scoreObj = new JSONObject();
        List<Float> nse = new ArrayList<>();
        List<Float> r2 = new ArrayList<>();
        List<Float> log = new ArrayList<>();
        List<Float> drms = new ArrayList<>();
        List<Float> roce = new ArrayList<>();
        List<Float> qre = new ArrayList<>();
        List<Float> re = new ArrayList<>();
        String filePath = resourcePath + "/" + pid +"obj_"+ eventName+".dat";
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "utf-8"));
        String line = reader.readLine(); // 第一行为标注行，记录了各个指标的名称
        while ((line = reader.readLine())!=null){
            String[] items = line.split("\t");
            nse.add(Float.parseFloat(items[0]));
            r2.add(Float.parseFloat(items[1]));
            log.add(Float.parseFloat(items[2]));
            drms.add(Float.parseFloat(items[3]));
            roce.add(Float.parseFloat(items[4]));
            qre.add(Float.parseFloat(items[5]));
            re.add(Float.parseFloat(items[6]));
        }
        scoreObj.put("Nash",nse);
        scoreObj.put("RSquared",r2);
        scoreObj.put("Log",log);
        scoreObj.put("DRMS",drms);
        scoreObj.put("ROCE",roce);
        scoreObj.put("QRE",qre);
        scoreObj.put("RE",re);
        scoreObj.put("Event",eventName);

        // 读取观测值  一起返回
        List<Float> obs = new ArrayList<>();
        String obsPath = resourcePath + "/" + pid + "obs_"+eventName+".txt";
        reader = new BufferedReader(new InputStreamReader(new FileInputStream(obsPath), "utf-8"));
        line = null;
        while ((line = reader.readLine())!= null){
            if (!line.startsWith("#")){
                String[] items = line.split(" ");
                obs.add(Float.parseFloat(items[0]));
            }
        }
        scoreObj.put("Observed",obs);
        return scoreObj;
    }

    public void clearSASimResult(String pid) {
        RestTemplate restTemplate = new RestTemplate();

        List<Task> taskList = taskDao.findAllByProjectId(pid);
        for (int i = 0; i < taskList.size(); i++) {
            List<TaskData> outputs = taskList.get(i).getOutputs();

            for (int j = 0; j < outputs.size(); j++) {
                TaskData state = outputs.get(j);
                String url = state.getUrl();
                if (url != ""){
                    String delUrl = url.substring(0,url.indexOf("?"));
                    restTemplate.delete(delUrl);
                }
            }
        }
    }
}
