package com.opengms.sabackproject.service;

import com.opengms.sabackproject.dao.ExperienceLibraryDao;
import com.opengms.sabackproject.entity.ExperienceLibrary;
import com.opengms.sabackproject.entity.UploadFile;
import org.bson.types.Binary;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.time.LocalDateTime;

@Service
public class ExperienceLibraryService {
    @Autowired
    ExperienceLibraryDao libraryDao;

    public ExperienceLibrary[] getLibrariesByModel(String model){
        return libraryDao.getAllByModel(model);
    }

    public ExperienceLibrary[] getLibraries(){
        return libraryDao.findAll().toArray(new ExperienceLibrary[0]);
    }

    public UploadFile[] convert(MultipartFile[] files) throws IOException {
        UploadFile[] uploadFiles = new UploadFile[files.length];

        for (int i = 0; i < files.length; i++) {
            MultipartFile f = files[i];

            UploadFile uploadFile = new UploadFile();
            uploadFile.setName(f.getOriginalFilename());
            uploadFile.setCreatedTime(LocalDateTime.now());
            uploadFile.setContent(new Binary(f.getBytes()));
            uploadFile.setContentType(f.getContentType());
            uploadFile.setSize(f.getSize());

            uploadFiles[i] = uploadFile;
        }
        return uploadFiles;
    }

    public void saveLibrary(ExperienceLibrary newLibrary) {
        libraryDao.save(newLibrary);
    }
}
