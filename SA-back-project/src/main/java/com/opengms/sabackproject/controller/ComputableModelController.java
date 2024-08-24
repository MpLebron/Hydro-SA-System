package com.opengms.sabackproject.controller;

import com.opengms.sabackproject.bean.JsonResult;
import com.opengms.sabackproject.entity.ComputableModel;
import com.opengms.sabackproject.service.ComputableModelService;
import com.opengms.sabackproject.utils.ResultUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@RestController
@RequestMapping("/computableModel")
public class ComputableModelController {

    @Autowired
    ComputableModelService computableModelService;

    @RequestMapping(value = "/allModel",method = RequestMethod.GET)
    public JsonResult getAll(){
        List<ComputableModel> models = computableModelService.getAllModel();
        return ResultUtils.success(models);
    }

    /**
     *  计算模型上传接口
     *  TODO
     *  代码参考test文件夹下测试函数 saveComputableModels
     */

}
