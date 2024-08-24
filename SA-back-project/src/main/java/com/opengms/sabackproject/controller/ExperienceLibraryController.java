package com.opengms.sabackproject.controller;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.opengms.sabackproject.bean.JsonResult;
import com.opengms.sabackproject.entity.ExperienceLibrary;
import com.opengms.sabackproject.entity.UploadFile;
import com.opengms.sabackproject.service.ExperienceLibraryService;
import com.opengms.sabackproject.utils.ResultUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
@RequestMapping("/experienceLibrary")
public class ExperienceLibraryController {
    @Autowired
    ExperienceLibraryService libraryService;

    @RequestMapping(value = "/allLibraryByModel",method = RequestMethod.GET)
    public JsonResult getAllLibraryByModel(@RequestParam("model") String model){
        ExperienceLibrary[] libraries = libraryService.getLibrariesByModel(model);
        return ResultUtils.success(libraries);
    }

    @RequestMapping(value = "/allLibrary", method = RequestMethod.GET)
    public JsonResult getAllLibrary(){
        ExperienceLibrary[] libraries = libraryService.getLibraries();
        return ResultUtils.success(libraries);
    }

    @RequestMapping(value = "/contribute", method = RequestMethod.POST)
    public JsonResult contributeLibrary(@RequestParam("library") String library,
                                        @RequestParam("files") MultipartFile[] files) throws IOException {
        System.out.println(library);
        ExperienceLibrary newLibrary = JSON.parseObject(library, ExperienceLibrary.class);
        UploadFile[] uploadFiles = libraryService.convert(files);
        newLibrary.setSaResults(uploadFiles);
        libraryService.saveLibrary(newLibrary);
        return ResultUtils.success();
    }
}
