package com.opengms.sabackproject;

import com.opengms.sabackproject.dao.ComputableModelDao;
import com.opengms.sabackproject.dao.ExperienceLibraryDao;
import com.opengms.sabackproject.dao.TaskDao;
import com.opengms.sabackproject.entity.ComputableModel;
import com.opengms.sabackproject.entity.ExperienceLibrary;
import com.opengms.sabackproject.entity.Task;
import com.opengms.sabackproject.entity.UploadFile;
import com.opengms.sabackproject.entity.support.TaskData;
import com.opengms.sabackproject.utils.Utils;
import org.bson.types.Binary;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@SpringBootTest
class SaBackProjectApplicationTests {

    @Autowired
    ComputableModelDao computableModelDao;

    @Autowired
    ExperienceLibraryDao experienceLibraryDao;

    @Autowired
    TaskDao taskDao;

    @Value("${resourcePath}")
    private String resourcePath;

    @Test
    void contextLoads() {
    }

    @Test
    void saveExperienceLibrary() throws IOException {
        ExperienceLibrary library = new ExperienceLibrary();
        library.setModel("SWAT");
        library.setResearchArea("湘江流域地处东经110°30′-114°00′，北纬24°31′-28°45′，干流全长856km，流域面积为94660km²，文中以湘江湘潭水文站上游流域为研究区域，面积为69706.7km²，地形特点为西南高东北低。气候属于中亚热带季风湿润气候，年均降水量为1300mm-1500mm。");
        library.setModelParams(new String[]{"GWQMN","HRU_SLP","ALPHA_BF","SFTMP"});
        library.setModelParamsRange("经验值上下波动20%");
        library.setSaMethods("CUP中的OAT分析和LH-OAT");
        library.setObjectiveFun("相对误差Re、相关系数R²和Nash");
        library.setSource("基于SWAT模型的湘江流域非源污染特征研究 赵新娜");
        library.setSourceUrl("https://www.baidu.com/");
        // 结果图
        File file = new File("C:\\Users\\Administrator\\Pictures\\2D.jpg");
        MultipartFile mulFile = new MockMultipartFile(
                "2D.jpg",
                "2D.jpg",
                "jpg",
                new FileInputStream(file)
        );
        UploadFile uploadFile = new UploadFile();
        uploadFile.setName(mulFile.getName());
        uploadFile.setCreatedTime(LocalDateTime.now());
        uploadFile.setContent(new Binary(mulFile.getBytes()));
        uploadFile.setContentType(mulFile.getContentType());
        uploadFile.setSize(mulFile.getSize());
        UploadFile[] uploadFiles = {uploadFile};
        library.setSaResults(uploadFiles);
        // GeoJSON
        library.setGeoJsonName("lev05-2950");
        File geoFile = new File("I:\\System-preparation\\a-DATA\\River\\GeoJSON\\lev05-2950.geojson");
        BufferedReader reader = new BufferedReader(new FileReader(geoFile));
        String tmp = reader.readLine();
        reader.close();
        library.setGeoJson(tmp);
        System.out.println(library);

        experienceLibraryDao.save(library);
    }

    @Test
    void saveComputableModels(){
        ComputableModel model = new ComputableModel();
        model.setOid(UUID.randomUUID().toString());
        model.setName("SWMM");
        model.setDescription("1");
        model.setMd5(UUID.randomUUID().toString());
        String mdl = "<ModelClass name=\"SWMM\" uid=\"7b40f051-17c2-4129-856f-e341eb1d5588\" style=\"SimpleCalculation\"><AttributeSet><Categories><Category principle=\"SWMM\" path=\"SWMM\"/></Categories><LocalAttributes><LocalAttribute local=\"EN_US\" localName=\"SWMM\" wiki=\"\"><Keywords>Storm,Water,Management,System</Keywords><Abstract>The EPA Storm Water Management Model (SWMM) is a dynamic rainfall-runoff simulation model used for single event or long-term (continuous) simulation of runoff quantity and quality from primarily urban areas.</Abstract></LocalAttribute></LocalAttributes></AttributeSet><Behavior><RelatedDatasets><DatasetItem name=\"inpData\" type=\"internal\" description=\"This is the inpData file of input data.\"><UdxDeclaration><UdxNode/></UdxDeclaration></DatasetItem><DatasetItem name=\"NodeID\" type=\"internal\" description=\"Node名称\"><UdxDeclaration><UdxNode><UdxNode name=\"NodeID\" type=\"DTKT_STRING\" description=\"名称\"/></UdxNode></UdxDeclaration></DatasetItem><DatasetItem name=\"LinkID\" type=\"internal\" description=\"Link名称\"><UdxDeclaration><UdxNode><UdxNode name=\"LinkID\" type=\"DTKT_STRING\" description=\"名称\"/></UdxNode></UdxDeclaration></DatasetItem><DatasetItem name=\"input\" type=\"internal\" description=\"Observation\"><UdxDeclaration><UdxNode/></UdxDeclaration></DatasetItem><DatasetItem name=\"SA_Param\" type=\"internal\" description=\"This is the parameter of SWMM.\"><UdxDeclaration><UdxNode name=\"Param\" type=\"DTKT_ANY\"><UdxNode name=\"Operation\" type=\"DTKT_STRING\" description=\"\"/><UdxNode name=\"Value\" type=\"DTKT_REAL\" description=\"\"/></UdxNode></UdxDeclaration></DatasetItem><DatasetItem name=\"rptData\" type=\"internal\" description=\"This is the rptData file of output data.\"><UdxDeclaration><UdxNode/></UdxDeclaration></DatasetItem><DatasetItem name=\"dispData\" type=\"internal\" description=\"This is the output file for display.\"><UdxDeclaration><UdxNode/></UdxDeclaration></DatasetItem></RelatedDatasets><StateGroup><States><State id=\"61a0269c-c142-42e4-b1cd-a362f561e170\" name=\"SWMM Data\" type=\"basic\" description=\"The inpData of SwmmModel\"><Event name=\"inpData\" type=\"response\" optional=\"False\" description=\"This is the inpData file of input data.\"><ResponseParameter datasetReference=\"inpData\" description=\"Load\"/></Event><Event name=\"NodeID\" type=\"response\" optional=\"True\" description=\"节点编号\"><ResponseParameter datasetReference=\"NodeID\" description=\"编号\"/></Event><Event name=\"LinkID\" type=\"response\" optional=\"True\" description=\"管道编号\"><ResponseParameter datasetReference=\"LinkID\" description=\"编号\"/></Event></State><State id=\"54ee5eb1-d9b4-4e05-afc6-873d77b7c61a\" name=\"Observation\" type=\"basic\" description=\"各个模拟目标的实测数据\"><Event name=\"Node-Inflow\" type=\"response\" optional=\"True\" description=\"Node-Inflow的实测数据，格式要求\"><ResponseParameter datasetReference=\"input\" description=\"Node-Inflow的实测数据\"/></Event><Event name=\"Node-Flooding\" type=\"response\" optional=\"True\" description=\"Node-Flooding的实测数据，格式要求\"><ResponseParameter datasetReference=\"input\" description=\"Node-Flooding的实测数据\"/></Event><Event name=\"Node-Depth\" type=\"response\" optional=\"True\" description=\"Node-Depth的实测数据，格式要求\"><ResponseParameter datasetReference=\"input\" description=\"Node-Depth的实测数据\"/></Event><Event name=\"Node-Head\" type=\"response\" optional=\"True\" description=\"Node-Head的实测数据，格式要求\"><ResponseParameter datasetReference=\"input\" description=\"Node-Head的实测数据\"/></Event><Event name=\"Link-Flow\" type=\"response\" optional=\"True\" description=\"Link-Flow的实测数据，格式要求\"><ResponseParameter datasetReference=\"input\" description=\"Link-Flow的实测数据\"/></Event><Event name=\"Link-Velocity\" type=\"response\" optional=\"True\" description=\"Link-Velocity的实测数据，格式要求\"><ResponseParameter datasetReference=\"input\" description=\"Link-Velocity的实测数据\"/></Event><Event name=\"Link-Depth\" type=\"response\" optional=\"True\" description=\"Link-Depth的实测数据，格式要求\"><ResponseParameter datasetReference=\"input\" description=\"Link-Depth的实测数据\"/></Event><Event name=\"Link-Capacity\" type=\"response\" optional=\"True\" description=\"Link-Capacity的实测数据，格式要求\"><ResponseParameter datasetReference=\"input\" description=\"Link-Capacity的实测数据\"/></Event></State><State id=\"f014fd62-48cc-4033-a708-add88f8b1d91\" name=\"Related to Confluence\" type=\"group\" description=\"汇流相关参数\"><Event name=\"N-Imperv\" type=\"response\" optional=\"True\" description=\"不透水区曼宁系数(Manning coefficient of impervious zone, N-Imperv) 0.01~0.04\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event><Event name=\"N-Perv\" type=\"response\" optional=\"True\" description=\"透水区曼宁系数(Manning coefficient of pervious zone, N-Perv) 0.1~0.35\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event><Event name=\"S-Imperv\" type=\"response\" optional=\"True\" description=\"不透水区洼地蓄水深度(Water storage depth of depression in impervious area, Dstore-Imperv\\S-Imperv)mm 0.2~2.54\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event><Event name=\"S-Perv\" type=\"response\" optional=\"True\" description=\"透水区洼地蓄水深度(Depression storage capacity of pervious area, Dstore- Perv\\S-Perv)mm 2~15\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event><Event name=\"PctZero\" type=\"response\" optional=\"True\" description=\"不透水区无填洼量比例(Percent of non-filled depressions in impervious area, %Zreo-Imperv\\PctZero) % 5~20\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event></State><State id=\"591b0153-e21b-494f-8d11-21d5b3c2b0d9\" name=\"Related to Infiltration\" type=\"group\" description=\"下渗相关参数\"><Event name=\"MaxRate\" type=\"response\" optional=\"True\" description=\"Horton公式最大入渗率(Horton formula maximum infiltration rate, MaxRate)mm/hr 72~78\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event><Event name=\"MinRate\" type=\"response\" optional=\"True\" description=\"Horton公式最小入渗率(Horton formula minimum infiltration rate, MinRate)mm/hr 3.1~3.8\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event><Event name=\"Decay\" type=\"response\" optional=\"True\" description=\"Horton公式衰减常数(Horton formula decay constant, Decay)L/h 2~4\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event><Event name=\"DryTime\" type=\"response\" optional=\"True\" description=\"干旱时间(Drought time, DryTime)/d 2~14\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event></State><State id=\"6d658c86-1e65-47a1-b73e-b920bea9a893\" name=\"Related to Transport\" type=\"group\" description=\"输送水力相关参数\"><Event name=\"Roughness\" type=\"response\" optional=\"True\" description=\"管道曼宁（糙率）系数(Manning coefficient of conduit, Roughness/Manning-N) 0.011~0.024\"><ResponseParameter datasetReference=\"SA_Param\" description=\"Load\"/></Event></State><State id=\"09ed2f40-1b5a-4485-8843-72eb0b95a618\" name=\"Result\" type=\"basic\" description=\"The Result of SwmmModel\"><Event name=\"rptData\" type=\"noresponse\" optional=\"False\" description=\"This is the rptData file of output data.\"><DispatchParameter datasetReference=\"rptData\" description=\"Export\"/></Event><Event name=\"outputForDisplay\" type=\"noresponse\" optional=\"False\" description=\"This is the output file for display. http://geomodeling.njnu.edu.cn/\"><DispatchParameter datasetReference=\"dispData\" description=\"Export\"/></Event></State></States><StateTransitions/></StateGroup></Behavior><Runtime name=\"SwmmModel\" version=\"1.0\" baseDir=\"$(ModelServicePath)\\SwmmModel\" entry=\"SwmmModel.exe\"><HardwareConfigures><Add key=\"memory size\" value=\"[500M,infinite)\"/><Add key=\"disk avail size\" value=\"[1GB,infinite)\"/></HardwareConfigures><SoftwareConfigures><Add key=\"Operation Platform\" value=\"Windows\"/><Add key=\"Language Platform\" value=\"Pascal\"/></SoftwareConfigures><Assemblies><Assembly name=\"swmm5.exe\" path=\"$(Assembly)\\SwmmModel\\\"/></Assemblies><SupportiveResources/></Runtime></ModelClass>\n";
        model.setMdl(mdl);
        model.setMdlJson(Utils.convertMdl(mdl));

        computableModelDao.save(model);
    }

    @Test
    void test() throws IOException {
        RestTemplate restTemplate = new RestTemplate();
        String pid = "ad11a543-437e-4b91-acf5-424b77abed0b";
        List<Task> taskList = taskDao.findAllByProjectId(pid);
        for (int i = 0; i < taskList.size(); i++) {
            List<TaskData> outputs = taskList.get(i).getOutputs();

            for (int j = 0; j < outputs.size(); j++) {
                TaskData state = outputs.get(j);
                String url = state.getUrl();
                if (url != ""){
                    String delUrl = url.substring(0,url.indexOf("?"));
                    System.out.println(delUrl);
                    restTemplate.delete(delUrl);
                }
            }
        }
    }
}
