package com.opengms.sabackproject.controller;

import com.alibaba.fastjson.JSONObject;
import com.opengms.sabackproject.bean.JsonResult;
import com.opengms.sabackproject.exception.MyException;
import com.opengms.sabackproject.utils.ResultUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
@RequestMapping(value = "/dataManager")
public class DataMangerController {

    //远程数据容器地址
    @Value("${dataContainerIpAndPort}")
    String dataContainerIpAndPort;

    @RequestMapping (value="/uploadMutiFiles",method = RequestMethod.POST)
    public JsonResult uploadMutiFiles(@RequestParam("datafile") MultipartFile[] files,
                                      @RequestParam("name")String uploadName,
                                      @RequestParam("userId")String userName,
                                      @RequestParam("serverNode")String serverNode,
                                      @RequestParam("origination")String origination ) throws IOException {

        String url="http://"+ dataContainerIpAndPort +"/data";

        RestTemplate restTemplate = new RestTemplate();

        MultiValueMap<String, Object> part = new LinkedMultiValueMap<>();

        for(int i=0;i<files.length;i++)
            part.add("datafile", files[i].getResource());
        part.add("name", uploadName);
        part.add("userId", userName);
        part.add("serverNode", serverNode);
        part.add("origination", origination);

        JSONObject jsonObject = restTemplate.postForObject(url, part, JSONObject.class);

        part=null;
        files=null;
        if(jsonObject.getIntValue("code")==-1){
            throw new MyException("远程服务出错");
        }
        JSONObject data = jsonObject.getJSONObject("data");
        data.put("ipAndPort",dataContainerIpAndPort);

        return ResultUtils.success(data);

    }
}
